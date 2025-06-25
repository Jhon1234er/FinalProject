from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from Izelapp.forms import *
from Izelapp.models import *
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from datetime import datetime, timedelta
import locale
import json
from Izelapp.utils import enviar_correo_recuperacion
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.urls import reverse
from django.utils.timezone import now
from django.views.decorators.csrf import csrf_exempt
from django.utils.deprecation import MiddlewareMixin

Usuario = get_user_model()

# Configura el locale para fechas en español (puede variar según tu sistema)
try:
    locale.setlocale(locale.LC_TIME, 'Spanish_Colombia.1252')
except locale.Error:
    pass

# region Home
def home(request):
    return render(request, 'home.html')

def sobre_nosotros(request):
    return render(request, 'paginas/Sobrenosotros.html')

def servicios(request):
    return render(request, 'paginas/Servicios.html')
# endregion

#region sesion expirada
def sesion_expirada(request):
    return render(request, 'sesion_expirada.html')
# endregion

# region login
def login_usuario(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not username or not password:
            return render(request, 'login.html', {
                'mensaje_error': 'Por favor, complete todos los campos.'
            })

        usuario = authenticate(request, username=username, password=password)
        if usuario is not None:
            login(request, usuario)

            # Redirección según el tipo de usuario
            if hasattr(usuario, 'medico'):
                return redirect('perfil_medico')
            elif hasattr(usuario, 'paciente'):
                return redirect('perfil_paciente')
            elif hasattr(usuario, 'administrador'):
                return redirect('perfil_administrador')
        else:
            return render(request, 'login.html', {
                'mensaje_error': 'Credenciales incorrectas, intente de nuevo o consulte con el administrador.'
            })

    return render(request, 'login.html')



class SessionExpiredMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.user.is_authenticated:
            return  # sesión activa

        if request.path.startswith('/admin/'):
            return  # ignora admin

        # Guarda última URL visitada antes de expirar
        if 'sesion_expirada' not in request.path and not request.path.startswith('/static/'):
            if request.session.get('was_logged_in', False):
                return redirect('sesion_expirada')

    def process_response(self, request, response):
        if request.user.is_authenticated:
            request.session['was_logged_in'] = True
        else:
            request.session['was_logged_in'] = False
        return response


def recuperar_contrasena(request):
    return render(request, 'usuario/recuperar.html')

@csrf_exempt
def buscar_usuario(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        tipo_doc = data.get('tipo_doc')
        num_doc = data.get('num_doc')

        try:
            usuario = Usuario.objects.get(tipo_doc=tipo_doc, num_doc=num_doc)
            return JsonResponse({'email': usuario.email, 'id': usuario.id})
        except Usuario.DoesNotExist:
            return JsonResponse({'error': 'Usuario no encontrado'}, status=404)

def restablecer_contrasena(request, id):
    usuario = get_object_or_404(Usuario, id=id)
    
    if request.method == "POST":
        nueva = request.POST.get("nueva_contrasena")
        repetir = request.POST.get("repetir_contrasena")

        if nueva == repetir:
            usuario.set_password(nueva)
            usuario.save()
            return render(request, "usuario/restablecer_exito.html", {"email": usuario.email})
        else:
            return render(request, "usuario/restablecer.html", {"error": "Las contraseñas no coinciden", "id": id})

    return render(request, "usuario/restablecer.html", {"id": id})
@login_required
def detallar_usuario(request):
    usuario = request.user
    if hasattr(usuario, 'medico'):
        tipo_usuario = 'medico'
        template = 'medico/detallar.html'
    elif hasattr(usuario, 'administrador'):
        tipo_usuario = 'administrador'
        template = 'administrador/detallar.html'
    elif hasattr(usuario, 'paciente'):
        tipo_usuario = 'paciente'
        template = 'paciente/detallar.html'
    else:
        return render(request, 'usuario/error.html', {'mensaje': 'Usuario no tiene un tipo válido asignado'})

    if request.method == 'POST':
        formulario = ImagenUserForm(request.POST, request.FILES, instance=usuario)
        if formulario.is_valid():
            formulario.save()
            return render(request, template, {'formulario': formulario, 'tipo_usuario': tipo_usuario, 'usuario': usuario, 'mensaje': 'Imagen de usuario actualizada correctamente.'})
    else:
        formulario = ImagenUserForm(instance=usuario)

    return render(request, template, {'formulario': formulario, 'tipo_usuario': tipo_usuario, 'usuario': usuario})

@login_required
def ver_mi_cita(request):
    paciente = request.user.paciente
    ahora = timezone.now()
    modo = request.GET.get('modo', 'activas')  # Puede ser 'activas' o 'perdidas'

    # Marcar como perdidas las que ya pasaron y estaban agendadas
    citas_vencidas = Cita.objects.filter(
        paciente=paciente,
        estado_cita='agendada',
        fecha_cita__lt=ahora.date()
    ) | Cita.objects.filter(
        paciente=paciente,
        estado_cita='agendada',
        fecha_cita=ahora.date(),
        hora_cita__lt=ahora.time()
    )

    for cita in citas_vencidas:
        cita.estado_cita = 'perdida'
        cita.save()

    # Filtrar según lo que se desea ver
    if modo == 'perdidas':
        citas = Cita.objects.filter(paciente=paciente, estado_cita='perdida').order_by('-fecha_cita', '-hora_cita')
    else:
        citas = Cita.objects.filter(paciente=paciente, estado_cita='agendada').order_by('-fecha_cita', '-hora_cita')

    return render(request, 'paciente/ver_cita.html', {
        'citas': citas,
        'modo': modo,
    })
@login_required
def citas_perdidas(request):
    paciente = request.user.paciente
    citas = Cita.objects.filter(paciente=paciente, estado_cita='perdida').order_by('-fecha_cita')
    return render(request, 'paciente/citas_perdidas.html', {'citas': citas})

def logout_usuario(request):
    logout(request)
    messages.success(request, 'Has cerrado sesión exitosamente.')
    return redirect('home')
# endregion

# region Usuario
def registrar_usuario(request):
    if request.method == 'POST':
        formulario = UsuarioForm(request.POST)
        if formulario.is_valid():
            usuario = formulario.save(commit=False)
            usuario.set_password(formulario.cleaned_data['password'])
            usuario.save()
            messages.success(request, 'Usuario creado exitosamente.')
        else:
            messages.error(request, 'Hay algunos errores en el registro. Vuelva a intentar...')
    else:
        formulario = UsuarioForm()
    return render(request, 'usuario/insertar.html', {'formulario': formulario})

def actualizar_usuario(request, id):
    usuario = get_object_or_404(Usuario, id=id)
    if request.method == 'POST':
        formulario = UsuarioForm(request.POST, instance=usuario)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, 'Usuario actualizado exitosamente.')
            return redirect('listar_usuarios')
        else:
            messages.error(request, 'Por favor, revisa los campos del formulario.')
    else:
        formulario = UsuarioForm(instance=usuario)
    return render(request, 'usuario/actualizar.html', {'formulario': formulario})

def lista_usuario(request):
    usuarios = Usuario.objects.all().order_by('tipo_doc')  
    conteo = usuarios.count()  
    return render(request, 'usuario/lista.html', {'usuarios': usuarios, 'conteo': conteo})

def eliminar_usuario(request, id):
    usuario = get_object_or_404(Usuario, id=id)
    usuario.delete()
    messages.success(request, 'Usuario eliminado exitosamente.')
    return redirect('listar_usuarios')

def eliminar_imagen_usuario(request):
    usuario = request.user
    if usuario.imagen:
        usuario.imagen.delete()
        usuario.imagen = None
        usuario.save()
        messages.success(request, 'Imagen eliminada exitosamente')
    else:
        messages.error(request, 'No hay imagen para eliminar')
    return redirect('detallar_usuario')
# endregion

# region Paciente

@login_required
def perfil_paciente(request):
    if not request.user.is_authenticated:
        return redirect('login')

    usuario = request.user
    return render(request, 'paciente/perfil.html', {
        'usuario': usuario,
        'tipo_usuario': 'paciente'
    })



def registrar_paciente(request):
    if request.method == 'POST':
        formulario = PacienteForm(request.POST, request.FILES)
        if formulario.is_valid():
            paciente = formulario.save(commit=False)
            paciente.set_password(formulario.cleaned_data['password'])
            paciente.save()
            messages.success(request, 'Registro exitoso. Ahora puedes iniciar sesión.')
            return redirect('login')  # ← aquí es donde debes cambiar
        else:
            messages.error(request, 'Hay algunos errores en el registro. Vuelva a intentar...')
    else:
        formulario = PacienteForm()
    
    return render(request, 'paciente/insertar.html', {'formulario': formulario})

def lista_paciente(request):
    pacientes = Paciente.objects.all()
    conteo = pacientes.count()

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'paciente/lista.html', {
            'pacientes': pacientes,
            'conteo': conteo
        })
    return render(request, 'paciente/lista.html', {
        'pacientes': pacientes,
        'conteo': conteo
    })
@login_required
def actualizar_paciente(request, id):
    paciente = get_object_or_404(Paciente, id=id)
    if request.method == 'POST':
        formulario = PacienteUpdateForm(request.POST, instance=paciente)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, 'Datos actualizados exitosamente.')
            return redirect('detallar_usuario')
        else:
            messages.error(request, 'Por favor, revisa los campos del formulario.')
    else:
        formulario = PacienteUpdateForm(instance=paciente)
    return render(request, 'paciente/actualizar.html', {'formulario': formulario,
    'usuario': paciente})
@login_required
def eliminar_paciente(request, id):
    paciente = get_object_or_404(Paciente, id=id)
    paciente.delete()
    messages.success(request, 'Paciente eliminado exitosamente.')
    return redirect('listar_paciente')
# endregion


# region Historial Clinico paciente
@login_required
def historial_clinico(request):
    return render(request, 'paciente/historial_clinico.html')

def cargar_historial_modulo(request, modulo):
    paciente = request.user.paciente
    contexto = {}
    template = ''

    if modulo == 'citas':
        contexto['citas'] = Cita.objects.filter(paciente=paciente)
        template = 'cita/historial.html'

    elif modulo == 'antecedentes':
        contexto['antecedentes'] = Antecedente.objects.filter(paciente=paciente)
        template = 'antecedente/historial.html'

    elif modulo == 'vacunas':
        contexto['vacunas'] = Vacuna.objects.filter(paciente=paciente)
        template = 'vacuna/historial.html'

    elif modulo == 'datos_quirurgicos':
        contexto['datos_quirurgicos'] = DatoQuirurgico.objects.filter(paciente=paciente)
        template = 'dato_quirurgico/historial.html'

    elif modulo == 'datos_antropometricos':
        contexto['datos_antropometricos'] = DatoAntropometrico.objects.filter(paciente=paciente)
        template = 'dato_antropometrico/historial.html'

    elif modulo == 'incapacidades':
        contexto['incapacidades'] = CertificadoIncapacidad.objects.filter(paciente=paciente)
        template = 'certificado_incapacidad/historial.html'

    elif modulo == 'formulas_medicas':
        contexto['formulas'] = RecetaMedica.objects.filter(paciente=paciente)
        template = 'receta_medica/historial.html'

    elif modulo == 'ordenes_medicas':
        contexto['ordenes'] = OrdenMedica.objects.filter(paciente=paciente)
        template = 'orden_medica/historial.html'

    return render(request, template, contexto)
# endregion



# region Administrador 
@login_required
def perfil_administrador(request):
    return render(request, 'administrador/perfil.html', {
        'usuario': request.user,
        'tipo_usuario': 'administrador'
    })

def registrar_administrador(request):
    if request.method == 'POST':
        formulario = AdministradorForm(request.POST, request.FILES)
        if formulario.is_valid():
            administrador = formulario.save(commit=False)
            administrador.set_password(formulario.cleaned_data['password'])
            administrador.save()
            messages.success(request, 'Administrador creado exitosamente.')
            return redirect('registrar_administrador')      
        else:
            messages.error(request, 'Por favor, corrija los errores en el formulario.')
    else:
        formulario = AdministradorForm()
    return render(request, 'administrador/insertar.html', {'formulario': formulario})

def lista_administrador(request):
    administradores = Administrador.objects.all()
    return render(request, 'administrador/lista.html', {'administradores': administradores})

def actualizar_administrador(request, id):
    administrador = get_object_or_404(Administrador, id=id)
    if request.method == 'POST':
        formulario = AdministradorUpdateForm(request.POST, instance=administrador)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, 'Datos actualizados exitosamente.')
            return redirect('detallar_usuario')
        else:
            messages.error(request, 'Por favor, revisa los campos.')
    else:
        formulario = AdministradorUpdateForm(instance=administrador)
    return render(request, 'administrador/actualizar.html', {
    'formulario': formulario,
    'usuario': administrador})

def eliminar_administrador(request, id):
    administrador = get_object_or_404(Administrador, id=id)
    administrador.delete()
    messages.success(request, 'Administrador eliminado exitosamente.')
    return redirect('listar_administrador')
# endregion

# region  Medicos 
@login_required
def perfil_medico(request):
    medico = request.user.medico
    hoy = timezone.now().date()
    citas_hoy = Cita.objects.filter(medico=medico, fecha_cita=hoy, estado_cita='agendada')
    total_citas_hoy = citas_hoy.count()
    return render(request, 'medico/perfil.html', {
        'usuario': medico,
        'total_citas_hoy': total_citas_hoy
    })
def registrar_medico(request):
    if request.method == 'POST':
        formulario = MedicoForm(request.POST)
        if formulario.is_valid():
            medico = formulario.save(commit=False)
            medico.set_password(formulario.cleaned_data['password'])
            medico.save()
            messages.success(request, 'Médico registrado exitosamente.')
            return redirect('login')
        else:
            messages.error(request, 'Por favor, corrija los errores en el formulario.')
    else:
        formulario = MedicoForm()
    return render(request, 'medico/insertar.html', {'formulario': formulario})

def lista_medico(request):
    medicos = Medico.objects.all()

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'medico/lista.html', {
            'medicos': medicos
        })
    return render(request, 'medico/lista.html', {
        'medicos': medicos
    })
@login_required
def actualizar_medico(request, id):
    medico = get_object_or_404(Medico, id=id)
    if request.method == 'POST':
        formulario = MedicoUpdateForm(request.POST, instance=medico)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, 'Datos actualizados exitosamente.')
            return redirect('detallar_usuario')
        else:
            messages.error(request, 'Por favor, revisa los campos.')
    else:
        formulario = MedicoUpdateForm(instance=medico)
    return render(request, 'medico/actualizar.html', {
        'formulario': formulario,
        'usuario': medico  
    })
def eliminar_medico(request, id):
    medico = get_object_or_404(Medico, id=id)
    medico.delete()
    messages.success(request, 'Médico eliminado exitosamente.')
    return redirect('listar_medico')
# endregion

# region Consulta 
def registrar_consulta(request):
    if request.method == 'POST':
        formulario_consulta = ConsultaForm(request.POST)
        formulario_atp = DatoAntropometricoForm(request.POST)
        if formulario_consulta.is_valid() and formulario_atp.is_valid():
            formulario_consulta.save()
            formulario_atp.save()
            messages.success(request, 'Consulta y datos antropométricos registrados exitosamente.')
            return redirect('registrar_consulta')
        else:
            messages.error(request, 'Por favor, llena todos los campos correctamente.')
    else:
        formulario_consulta = ConsultaForm()
        formulario_atp = DatoAntropometricoForm()
    return render(request, 'consulta/insertar.html', {
        'formulario_consulta': formulario_consulta,
        'formulario_atp': formulario_atp,
    })

def lista_consulta(request, paciente_id):
    paciente = get_object_or_404(Paciente, id=paciente_id)
    consultas = Consulta.objects.filter(paciente=paciente)
    return render(request, 'consulta/lista.html', {
        'consultas': consultas,
        'paciente': paciente
    })

def actualizar_consulta(request, id):
    consulta = get_object_or_404(Consulta, id=id)
    if request.method == 'POST':
        formulario = ConsultaForm(request.POST, instance=consulta)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, 'Consulta actualizada exitosamente.')
            return redirect('listar_consulta')
        else:
            messages.error(request, 'Por favor, revisa los campos del formulario.')
    else:
        formulario = ConsultaForm(instance=consulta)
    return render(request, 'consulta/actualizar.html', {'formulario': formulario})

def eliminar_consulta(request, id):
    consulta = get_object_or_404(Consulta, id=id)
    consulta.delete()
    messages.success(request, 'Consulta eliminada exitosamente.')
    return redirect('listar_consulta')
# endregion

# region PerfilPaciente 
def registrar_perfil_paciente(request):
    if request.method == 'POST':
        formulario = PerfilPacienteForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, 'Perfil de paciente creado exitosamente.')
            return redirect('crear_perfil_paciente')
        else:
            messages.error(request, 'Por favor, llena todos los campos.')
    else:
        formulario = PerfilPacienteForm()
    return render(request, 'perfil_paciente/crear.html', {'formulario': formulario})

def lista_perfil_paciente(request):
    perfiles = PerfilPaciente.objects.all()
    return render(request, 'perfil_paciente/lista.html', {'perfiles': perfiles})
# endregion

# region Vacuna 
@login_required
def registrar_vacuna(request):
    if request.method == 'POST':
        formulario = VacunaForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, 'Vacuna registrada exitosamente.')
            return redirect('crear_vacuna')
        else:
            messages.error(request, 'Por favor, llena todos los campos.')
    else:
        formulario = VacunaForm()
    return render(request, 'vacuna/crear.html', {'formulario': formulario})

@login_required
def lista_vacuna(request):
    vacunas = Vacuna.objects.all()
    return render(request, 'vacuna/lista.html', {'vacunas': vacunas})

@login_required
def eliminar_vacuna(request, id):
    vacuna = get_object_or_404(Vacuna, id=id)
    vacuna.delete()
    messages.success(request, 'Vacuna eliminada exitosamente.')
    return redirect('listar_vacuna')
# endregion

# region RecetaMedica 
@login_required
def registrar_receta_medica(request):
    if request.method == 'POST':
        formulario = RecetaMedicaForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, 'Receta médica registrada exitosamente.')
            return redirect('crear_receta_medica')
        else:
            messages.error(request, 'Por favor, llena todos los campos.')
    else:
        formulario = RecetaMedicaForm()
    return render(request, 'receta_medica/insertar.html', {'formulario': formulario})

def lista_receta_medica(request):
    recetas = RecetaMedica.objects.all()
    return render(request, 'receta_medica/lista.html', {'recetas': recetas})

def eliminar_receta_medica(request, id):
    receta = get_object_or_404(RecetaMedica, id=id)
    receta.delete()
    messages.success(request, 'Receta médica eliminada exitosamente.')
    return redirect('listar_receta_medica')
# endregion

# region Antecedentes
@login_required
def crear_antecedente(request):
    if request.method == 'POST':
        formulario = AntecedenteForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, 'Antecedente creado exitosamente.')
            return redirect('crear_antecedente')
        else:
            messages.error(request, 'Por favor, llena todos los campos.')
    else:
        formulario = AntecedenteForm()
    return render(request, 'antecedente/crear.html', {'formulario': formulario})

@login_required
def lista_antecedente(request):
    antecedentes = Antecedente.objects.all()
    return render(request, 'antecedente/lista.html', {'antecedentes': antecedentes})
# endregion

# region Quirurgico
@login_required
def registrar_dato_quirurgico(request):
    if request.method == 'POST':
        formulario = DatoQuirurgicoForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, 'Dato quirúrgico creado exitosamente.')
            return redirect('crear_dato_quirurgico')
        else:
            messages.error(request, 'Por favor, llena todos los campos.')
    else:
        formulario = DatoQuirurgicoForm()
    return render(request, 'dato_quirurgico/crear.html', {'formulario': formulario})

def lista_dato_quirurgico(request):
    datos_quirurgicos = DatoQuirurgico.objects.all()
    return render(request, 'dato_quirurgico/lista.html', {'datos_quirurgicos': datos_quirurgicos})
# endregion

# region Historial
@login_required
def registrar_historia_clinica(request):
    if request.method == 'POST':
        formulario = RegistroClinicoForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, 'Historia clínica creada exitosamente.')
            return redirect('crear_historia_clinica')
        else:
            messages.error(request, 'Por favor, llena todos los campos.')
    else:
        formulario = RegistroClinicoForm()
    return render(request, 'historia_clinica/crear.html', {'formulario': formulario})

@login_required
def lista_historia_clinica(request):
    historias_clinicas = HistoriaClinica.objects.all()
    return render(request, 'historia_clinica/lista.html', {'historias_clinicas': historias_clinicas})
# endregion

# region Antropometrico
@login_required
def registrar_dato_antropometrico(request):
    if request.method == 'POST':
        formulario = DatoAntropometricoForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, 'Dato antropométrico creado exitosamente.')
            return redirect('crear_dato_antropometrico')
        else:
            messages.error(request, 'Por favor, llena todos los campos.')
    else:
        formulario = DatoAntropometricoForm()
    return render(request, 'dato_antropometrico/insertar.html', {'formulario': formulario})

@login_required
def lista_dato_antropometrico(request):
    datos_antropometricos = DatoAntropometrico.objects.all()
    return render(request, 'dato_antropometrico/lista.html', {'datos_antropometricos': datos_antropometricos})
# endregion

# region Cita
@login_required
def registrar_cita(request):
    if request.method == 'POST':
        formulario = CitaForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, 'Cita creada exitosamente.')
            return redirect('registrar_cita')
        else:
            messages.error(request, 'Por favor, llena todos los campos.')
    else:
        formulario = CitaForm()
    return render(request, 'cita/insertar.html', {'formulario': formulario})

@login_required
def lista_cita(request):
    citas = Cita.objects.all()
    return render(request, 'cita/lista.html', {'citas': citas})


@login_required 
def consulta_medica(request, paciente_id, cita_id):
    paciente = get_object_or_404(Paciente, id=paciente_id)
    medico = request.user  
    cita = get_object_or_404(Cita, id=cita_id)
    return render(request, 'medico/consulta_medica.html', {
        'paciente': paciente,
        'medico': medico,
        'cita': cita
    })

@login_required
def get_form(request, form_name):
    form_classes = {
        'vacuna': VacunaForm,
        'consulta': ConsultaForm,
        'dato_antropometrico': DatoAntropometricoForm,
        'certificado_incapacidad': CertificadoIncapacidadForm,
        'orden_medica': OrdenMedicaForm,
        'receta_medica': RecetaMedicaForm,
        'perfil_paciente': PerfilPacienteForm,
        'antecedente': AntecedenteForm,
        'dato_quirurgico': DatoQuirurgicoForm,
    }
    form_class = form_classes.get(form_name)
    if form_class:
        form = form_class()
        return render(request, f'{form_name}/insertar.html', {'form': form})
    else:
        return JsonResponse({'error': 'Formulario no encontrado'}, status=404)

@csrf_protect
def submit_all(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Error en el formato JSON"}, status=400)

        paciente_id = data.get("paciente_id")
        cita_id = data.get("cita_id") 
        formularios = data.get("formularios", [])

        if not formularios:
            return JsonResponse({"error": "No se recibieron formularios"}, status=400)

        try:
            paciente = get_object_or_404(Paciente, id=paciente_id)
            medico = get_object_or_404(Medico, usuario_ptr=request.user)
        except (Paciente.DoesNotExist, Medico.DoesNotExist):
            return JsonResponse({"error": "Paciente o Médico no encontrado"}, status=404)

        for formulario in formularios:
            form_name = formulario.get("form_name")
            campos = formulario.get("data")
            form_class = {
                'vacuna': VacunaForm,
                'consulta': ConsultaForm,
                'dato_antropometrico': DatoAntropometricoForm,
                'certificado_incapacidad': CertificadoIncapacidadForm,
                'orden_medica': OrdenMedicaForm,
                'receta_medica': RecetaMedicaForm,
                'perfil_paciente': PerfilPacienteForm,
                'antecedente': AntecedenteForm,
                'dato_quirurgico': DatoQuirurgicoForm,
            }.get(form_name)
            if form_class:
                form = form_class(campos)
                if form.is_valid():
                    instancia = form.save(commit=False)
                    instancia.paciente = paciente
                    instancia.medico = medico
                    instancia.save()
                else:
                    return JsonResponse({
                        "error": f"Formulario '{form_name}' inválido",
                        "errores": form.errors
                    }, status=400)

        if cita_id:
            try:
                cita = Cita.objects.get(id=cita_id)
                cita.estado_cita = 'atendida'
                cita.save()
            except Cita.DoesNotExist:
                return JsonResponse({"error": "Cita no encontrada"}, status=404)

        return JsonResponse({
            "message": "Consulta finalizada correctamente",
            "redirect_url": reverse('agenda_citas_medico')
        })

    return JsonResponse({"error": "Método no permitido"}, status=405)

@login_required
def detalle_cita(request, cita_id):
    cita = get_object_or_404(Cita, id=cita_id)
    return render(request, 'cita/detalle_cita.html', {'cita': cita})

@login_required
def cancelar_cita(request, cita_id):
    cita = get_object_or_404(Cita, id=cita_id, paciente=request.user.paciente)

    if cita.fecha_cita == now().date() and cita.hora_cita <= (now() + timedelta(hours=1)).time():
        messages.error(request, "No puedes cancelar una cita con menos de 1 hora de anticipación.")
        return redirect('ver_mi_cita')

    disponibilidad = cita.disponibilidad
    cita.delete()

    if disponibilidad:
        disponibilidad.estado = 'disponible'
        disponibilidad.save()

    messages.success(request, "Cita cancelada exitosamente.")
    return redirect('ver_mi_cita')

# endregion

# region Incapacidad
@login_required
def registrar_certificado_incapacidad(request):
    if request.method == 'POST':
        formulario = CertificadoIncapacidadForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, 'Certificado de incapacidad creado exitosamente.')
            return redirect('crear_certificado_incapacidad')
        else:
            messages.error(request, 'Por favor, llena todos los campos.')
    else:
        formulario = CertificadoIncapacidadForm()
    return render(request, 'certificado_incapacidad/insertar.html', {'formulario': formulario})

@login_required
def lista_certificado_incapacidad(request):
    certificados = CertificadoIncapacidad.objects.all()
    return render(request, 'certificado_incapacidad/lista.html', {'certificados': certificados})
# endregion

# region OrdenMedica
@login_required
def registrar_orden_medica(request):
    if request.method == 'POST':
        formulario = OrdenMedicaForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, 'Orden médica creada exitosamente.')
            return redirect('crear_orden_medica')
        else:
            messages.error(request, 'Por favor, llena todos los campos.')
    else:
        formulario = OrdenMedicaForm()
    return render(request, 'orden_medica/insertar.html', {'formulario': formulario})

@login_required
def lista_orden_medica(request):
    ordenes = OrdenMedica.objects.all()
    return render(request, 'orden_medica/lista.html', {'ordenes': ordenes})
# endregion

# region Horario 
@login_required
def registrar_horario_medico(request):
    if request.method == 'POST':
        formulario = HorarioMedicoForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, 'Horario médico creado exitosamente.')
            return redirect('crear_horario_medico')
        else:
            messages.error(request, 'Por favor, llena todos los campos.')
    else:
        formulario = HorarioMedicoForm()
    return render(request, 'horario_medico/crear.html', {'formulario': formulario})

@login_required
def lista_horario_medico(request):
    horarios = HorarioMedico.objects.all()
    return render(request, 'horario_medico/lista.html', {'horarios': horarios})

@login_required
def actualizar_horario_medico(request, id):
    horario = get_object_or_404(HorarioMedico, id=id)
    if request.method == 'POST':
        formulario = HorarioMedicoForm(request.POST, instance=horario)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, 'Horario médico actualizado exitosamente.')
            return redirect('lista_horario_medico')
        else:
            messages.error(request, 'Por favor, revisa los campos.')
    else:
        formulario = HorarioMedicoForm(instance=horario)
    return render(request, 'horario_medico/actualizar.html', {'formulario': formulario})

@login_required
def eliminar_horario_medico(request, id):
    horario = get_object_or_404(HorarioMedico, id=id)
    horario.delete()
    messages.success(request, 'Horario médico eliminado exitosamente.')
    return redirect('lista_horario_medico')
# endregion

# region AGENDA
@login_required
def calendario(request):
    return render(request, 'cita/calendario.html')

@login_required
def obtener_disponibilidad(request):
    eventos = []
    for disponibilidad in Disponibilidad.objects.filter(estado='disponible'):
        eventos.append({
            'id': disponibilidad.id,
            'title': f'{disponibilidad.tipo_cita.capitalize()} - {disponibilidad.medico}',
            'start': f'{disponibilidad.fecha}T{disponibilidad.hora_inicio}',
            'end': f'{disponibilidad.fecha}T{disponibilidad.hora_fin}',
        })
    return JsonResponse(eventos, safe=False)

@login_required
def verificar_disponibilidad(request):
    fecha = request.GET.get('fecha')
    disponibilidad = Disponibilidad.objects.filter(fecha=fecha)
    if disponibilidad.exists():
        return JsonResponse({'disponible': True})
    return JsonResponse({'disponible': False})

@login_required
def confirmar_cita(request, disponibilidad_id):
    disponibilidad = get_object_or_404(Disponibilidad, pk=disponibilidad_id)
    if disponibilidad.estado != 'disponible':
        return render(request, 'cita/no_disponible.html', {'disponibilidad': disponibilidad})

    paciente = request.user.paciente
    inicio_nueva = datetime.combine(disponibilidad.fecha, disponibilidad.hora_inicio)
    fin_nueva = datetime.combine(disponibilidad.fecha, disponibilidad.hora_fin)
    citas_en_dia = Cita.objects.filter(
        paciente=paciente,
        fecha_cita=disponibilidad.fecha,
        estado_cita='agendada'  # <--- esto es clave
    )

    conflicto = False
    for cita in citas_en_dia:
        inicio_existente = datetime.combine(cita.fecha_cita, cita.hora_cita)
        fin_existente = inicio_existente + timedelta(minutes=30)
        if inicio_nueva < fin_existente and fin_nueva > inicio_existente:
            conflicto = True
            break
    if conflicto:
        return render(request, 'cita/no_disponible.html', {'disponibilidad': disponibilidad})

    if request.method == 'POST':
        # Crear la cita
        cita = Cita(
            paciente=paciente,
            medico=disponibilidad.medico,
            fecha_cita=disponibilidad.fecha,
            hora_cita=disponibilidad.hora_inicio,
            especialidad=disponibilidad.tipo_cita,
            estado_cita='agendada',
            disponibilidad=disponibilidad
        )
        cita.save()
        # Cambiar estado de la disponibilidad a "pendiente"
        disponibilidad.estado = 'pendiente'
        disponibilidad.save()
        messages.success(request, "Cita confirmada exitosamente.")
        return render(request, 'paciente/perfil.html')

    return render(request, 'cita/confirmar_cita.html', {
        'disponibilidad': [disponibilidad]
    })


@login_required
def generar_disponibilidad(request):
    if not request.user.is_authenticated or not hasattr(request.user, 'administrador'):
        return redirect('login')

    if request.method == 'POST':
        form = GenerarDisponibilidadForm(request.POST)
        if form.is_valid():
            # Médicos seleccionados visualmente (se reciben por campo oculto)
            medicos_ids = request.POST.get('medicos_seleccionados', '')
            if not medicos_ids:
                messages.error(request, "Debes seleccionar al menos un médico.")
                return render(request, 'cita/generar_disponibilidad.html', {'form': form})

            medicos = Medico.objects.filter(id__in=medicos_ids.split(','))

            fecha_inicio = form.cleaned_data['fecha_inicio']
            fecha_fin = form.cleaned_data['fecha_fin']
            dias_seleccionados = [int(d) for d in form.cleaned_data['dias']]
            hora_inicio = form.cleaned_data['hora_inicio']
            hora_fin = form.cleaned_data['hora_fin']
            duracion = int(form.cleaned_data['duracion'])

            bloques_enviados = request.POST.getlist('bloques')
            total_creadas = 0
            fecha_actual = fecha_inicio

            while fecha_actual <= fecha_fin:
                if fecha_actual.weekday() in dias_seleccionados:
                    for bloque in bloques_enviados:
                        desde_str, hasta_str = bloque.split('-')
                        desde = datetime.strptime(desde_str, "%H:%M").time()
                        hasta = datetime.strptime(hasta_str, "%H:%M").time()

                        for medico in medicos:
                            ya_existe = Disponibilidad.objects.filter(
                                medico=medico,
                                fecha=fecha_actual,
                                hora_inicio=desde,
                                hora_fin=hasta
                            ).exists()
                            if not ya_existe:
                                Disponibilidad.objects.create(
                                    medico=medico,
                                    fecha=fecha_actual,
                                    hora_inicio=desde,
                                    hora_fin=hasta,
                                    tipo_cita='general',
                                    estado='disponible'
                                )
                                total_creadas += 1
                fecha_actual += timedelta(days=1)

            messages.success(request, f"Se generaron {total_creadas} disponibilidades.")
            return redirect('perfil_administrador')
    else:
        form = GenerarDisponibilidadForm()

    return render(request, 'cita/gestionar_disponibilidad.html', {'form': form})
@login_required
def agenda_citas_medico(request):
    medico = request.user.medico  
    citas = Cita.objects.filter(
        medico=medico,
        estado_cita='agendada'
    ).order_by('fecha_cita', 'hora_cita')
    return render(request, 'medico/agenda.html', {'citas': citas})
# endregion

@login_required
def lista_citas_admin(request):
    if not hasattr(request.user, 'administrador'):
        return redirect('login')

    citas = Cita.objects.select_related('paciente', 'medico').all().order_by('-fecha_cita', '-hora_cita')

    # Verifica si es AJAX
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'admin/lista_citas.html', {'citas': citas})
    else:
        return render(request, 'admin/lista_citas_completa.html', {'citas': citas})
