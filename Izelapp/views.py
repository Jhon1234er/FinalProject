from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from Izelapp.forms import *
from Izelapp.models import *
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse,JsonResponse




#region Home
def home(request):
    return render(request, 'home.html')
#endregion
 





  
# region login
def login_usuario(request):
    if request.method == 'POST':
        username_recibido = request.POST.get('username')
        password_recibido = request.POST.get('password')

        if not username_recibido or not password_recibido:
            return render(request, 'login.html', {'mensaje_error': 'Por favor, complete todos los campos.'})

        usuario = authenticate(request, username=username_recibido, password=password_recibido)
        if usuario is not None:
            login(request, usuario)

            # Verificar si el usuario es Médico u otros roles
            if hasattr(request.user, 'medico'):
                return render(request, 'medico/perfil.html', {'tipo_usuario': 'Medico'})
            elif hasattr(request.user, 'paciente'):
                return render(request, 'paciente/perfil.html', {'tipo_usuario': 'Paciente'})
            elif hasattr(request.user, 'administrador'):
                return render(request, 'administrador/perfil.html', {'tipo_usuario': 'Administrador'})
            elif hasattr(request.user, 'ti'):
                return render(request, 'ti/perfil.html', {'tipo_usuario': 'TI'})
            elif hasattr(request.user, 'auxiliar'):
                return render (request, 'auxiliar/perfil.html', {'tipo_usuario': 'Auxiliar'})
        else:
            return render(request, 'login.html', {'mensaje_error': 'Credenciales incorrectas, intente de nuevo o consulte con Administrador de Usuarios'})

    return render(request, 'login.html')



@login_required
def detallar_usuario(request):
    usuario = request.user  # Obtener el usuario logueado

    # Inicializar 'template' y 'tipo_usuario' a None
    template = None
    tipo_usuario = None

    # Determinar el tipo de usuario y asignar el template correspondiente utilizando isinstance
    if hasattr(usuario, 'medico'):
        tipo_usuario = 'medico'
        template = 'medico/detallar.html'
    elif hasattr(usuario, 'administrador'):
        tipo_usuario = 'administrador'
        template = 'administrador/detallar.html'
    elif hasattr(usuario, 'auxiliar'):
        tipo_usuario = 'auxiliar'
        template = 'auxiliar/detallar.html'
    elif hasattr(usuario, 'ti'):
        tipo_usuario = 'ti'
        template = 'ti/detallar.html'
    elif hasattr(usuario, 'paciente'):
        tipo_usuario = 'paciente'
        template = 'paciente/detallar.html'

    # Si no se asignó un template, mostrar error
    if template is None:
        return render(request, 'usuario/error.html', {'mensaje': 'Usuario no tiene un tipo válido asignado'})

    # Si el template es válido, procesar el formulario
    if request.method == 'POST':
        formulario = ImagenUserForm(request.POST, request.FILES, instance=usuario)
        if formulario.is_valid():
            formulario.save()
            return render(request, template, {'formulario': formulario, 'tipo_usuario': tipo_usuario, 'mensaje': 'Imagen de usuario actualizada correctamente.'})
    else:
        formulario = ImagenUserForm(instance=usuario)

    # Renderizar el template correspondiente
    return render(request, template, {'formulario': formulario, 'tipo_usuario': tipo_usuario})





def logout_usuario(request):
    logout(request)
    messages.success(request, 'Has cerrado sesión exitosamente.')
    return redirect('home')



#endregion






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


#endregion






# region Paciente
def registrar_paciente(request):
    if request.method == 'POST':
        formulario = PacienteForm(request.POST, request.FILES)
        if formulario.is_valid():
            paciente = formulario.save(commit=False)
            # Cifra la contraseña utilizando set_password()
            paciente.set_password(formulario.cleaned_data['password'])
            paciente.save()
            messages.success(request, 'Paciente creado exitosamente.')
            return redirect('registrar_paciente')
        else:
            messages.error(request, 'Hay algunos errores en el registro. Vuelva a intentar...')
    else:
        formulario = PacienteForm()
    return render(request, 'paciente/insertar.html', {'formulario': formulario})



def lista_paciente(request):
    pacientes = Paciente.objects.all()
    return render(request, 'paciente/lista.html', {'pacientes': pacientes})

def actualizar_paciente(request, id):
    paciente = get_object_or_404(Paciente, id=id)
    if request.method == 'POST':
        formulario = PacienteForm(request.POST, instance=paciente)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, 'Paciente actualizado exitosamente.')
            return redirect('listar_paciente')
        else:
            messages.error(request, 'Por favor, revisa los campos del formulario.')
    else:
        formulario = PacienteForm(instance=paciente)
    return render(request, 'paciente/actualizar.html', {'formulario': formulario})

def eliminar_paciente(request, id):
    paciente = get_object_or_404(Paciente, id=id)
    paciente.delete()
    messages.success(request, 'Paciente eliminado exitosamente.')
    return redirect('listar_paciente')
#endregion







#region Administrador 
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
            messages.error(request, 'Por favor, complete todos los campos del administrador.')
    else:
        formulario = AdministradorForm()
    return render(request, 'administrador/insertar.html', {'formulario': formulario})


def lista_administrador(request):
    administradores = Administrador.objects.all()
    return render(request, 'administrador/lista.html', {'administradores': administradores})

def actualizar_administrador(request, id):
    administrador = get_object_or_404(Administrador, id=id)
    if request.method == 'POST':
        formulario = AdministradorForm(request.POST, instance=administrador)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, 'Administrador actualizado exitosamente.')
            return redirect('listar_administrador')
        else:
            messages.error(request, 'Por favor, revisa los campos.')
    else:
        formulario = AdministradorForm(instance=administrador)
    return render(request, 'administrador/actualizar.html', {'formulario': formulario})

def eliminar_administrador(request, id):
    administrador = get_object_or_404(Administrador, id=id)
    administrador.delete()
    messages.success(request, 'Administrador eliminado exitosamente.')
    return redirect('listar_administrador')
#endregion







#region TI 
def registrar_ti(request):
    if request.method == 'POST':
        formulario = TIForm(request.POST)
        if formulario.is_valid():
            ti = formulario.save(commit=False)
            ti.set_password(formulario.cleaned_data['password'])
            ti.save()
            messages.success(request, 'TI registrado exitosamente.')
            return redirect('listar_ti')  # Redirigir a la lista de TI
        else:
            messages.error(request, 'Por favor, complete todos los campos del TI.')
    else:
        formulario = TIForm()
    return render(request, 'ti/insertar.html', {'formulario': formulario})


def lista_ti(request):
    its = TI.objects.all()
    return render(request, 'ti/lista.html', {'its': its})

def actualizar_ti(request, id):
    ti = get_object_or_404(TI, id=id)
    if request.method == 'POST':
        formulario = TIForm(request.POST, instance=ti)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, 'TI actualizado exitosamente.')
            return redirect('listar_ti')
        else:
            messages.error(request, 'Por favor, revisa los campos.')
    else:
        formulario = TIForm(instance=ti)

    return render(request, 'ti/actualizar.html', {'formulario': formulario})

def eliminar_ti(request, id):
    ti= get_object_or_404(TI, id=id)
    ti.delete()
    messages.success(request, 'TI eliminado exitosamente.')
    return redirect('listar_ti')
#endregion








#region  Medicos 
def registrar_medico(request):
    if request.method == 'POST':
        formulario = MedicoForm(request.POST)
        if formulario.is_valid():
            medico = formulario.save(commit=False)
            medico.set_password(formulario.cleaned_data['password'])
            medico.save()
            messages.success(request, 'Médico registrado exitosamente.')
            return redirect('listar_medico')  # Redirigir a la lista de médicos
        else:
            messages.error(request, 'Por favor, complete todos los campos del médico.')
    else:
        formulario = MedicoForm()

    return render(request, 'medico/insertar.html', {'formulario': formulario})


def lista_medico(request):
    medicos = Medico.objects.all()
    return render(request, 'medico/lista.html', {'medicos': medicos})

def actualizar_medico(request, id):
    medico = get_object_or_404(Medico, id=id)
    if request.method == 'POST':
        formulario = MedicoForm(request.POST, instance=medico)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, 'Médico actualizado exitosamente.')
            return redirect('listar_medico')
        else:
            messages.error(request, 'Por favor, revisa los campos.')
    else:
        formulario = MedicoForm(instance=medico)
    return render(request, 'medico/actualizar.html', {'formulario': formulario})

def eliminar_medico(request, id):
    medico = get_object_or_404(Medico, id=id)
    medico.delete()
    messages.success(request, 'Médico eliminado exitosamente.')
    return redirect('listar_medico')
#endregion





#region Auxiliar
def registrar_auxiliar(request):
    if request.method == 'POST':
        formulario = AuxiliarForm(request.POST)
        if formulario.is_valid():
            auxiliar = formulario.save(commit=False)
            # Asociar el usuario al auxiliar
            usuario_id = request.POST.get('usuario')
            usuario = Usuario.objects.get(id=usuario_id)
            auxiliar.usuario = usuario
            auxiliar.save()
            messages.success(request, 'Auxiliar registrado exitosamente.')
            return redirect('listar_auxiliares')  # Redirigir a la lista de auxiliares
        else:
            messages.error(request, 'Por favor, complete todos los campos del auxiliar.')
    else:
        formulario = AuxiliarForm()

    return render(request, 'auxiliar/insertar.html', {'formulario': formulario})



def lista_auxiliar(request):
    auxiliares = Auxiliar.objects.all()  
    return render(request, 'auxiliar/lista.html', {'auxiliares': auxiliares})


def actualizar_auxiliar(request, id):
    auxiliar = get_object_or_404(Auxiliar, id=id)
    if request.method == 'POST':
        formulario = AuxiliarForm(request.POST, instance=auxiliar)
        if formulario.is_valid():
            formulario.save()
            return redirect('listar_auxiliares')  
    else:
        formulario = AuxiliarForm(instance=auxiliar)
    return render(request, 'auxiliar/actualizar.html', {'formulario': formulario})


def eliminar_auxiliar(request, id):
    auxiliar = get_object_or_404(Auxiliar, id=id)
    auxiliar.delete()
    return redirect('listar_auxiliares')
#endregion












#region Consulta 
def registrar_consulta(request):
    if request.method == 'POST':
        formulario = ConsultaForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, 'Consulta registrada exitosamente.')
            return redirect('crear_consulta')
        else:
            messages.error(request, 'Por favor, llena todos los campos.')
    else:
        formulario = ConsultaForm()
    return render(request, 'consulta/crear.html', {'formulario': formulario})

def lista_consulta(request):
    consultas = Consulta.objects.all()
    return render(request, 'consulta/lista.html', {'consultas': consultas})

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
#endregion







#region PerfilPaciente 
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
#endregion







#region Vacuna 
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

def lista_vacuna(request):
    vacunas = Vacuna.objects.all()
    return render(request, 'vacuna/lista.html', {'vacunas': vacunas})

def eliminar_vacuna(request, id):
    vacuna = get_object_or_404(Vacuna, id=id)
    vacuna.delete()
    messages.success(request, 'Vacuna eliminada exitosamente.')
    return redirect('listar_vacuna')
#endregion







#region RecetaMedica 
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
    return render(request, 'receta_medica/crear.html', {'formulario': formulario})

def lista_receta_medica(request):
    recetas = RecetaMedica.objects.all()
    return render(request, 'receta_medica/lista.html', {'recetas': recetas})

def eliminar_receta_medica(request, id):
    receta = get_object_or_404(RecetaMedica, id=id)
    receta.delete()
    messages.success(request, 'Receta médica eliminada exitosamente.')
    return redirect('listar_receta_medica')
#endregion







#region Antecedentes
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

def lista_antecedente(request):
    antecedentes = Antecedente.objects.all()
    return render(request, 'antecedente/lista.html', {'antecedentes': antecedentes})
#endregion







#region Quirurgico
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
#endregion







#region Historial
def registrar_historia_clinica(request):
    if request.method == 'POST':
        formulario = HistoriaClinicaForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, 'Historia clínica creada exitosamente.')
            return redirect('crear_historia_clinica')
        else:
            messages.error(request, 'Por favor, llena todos los campos.')
    else:
        formulario = HistoriaClinicaForm()
    return render(request, 'historia_clinica/crear.html', {'formulario': formulario})

def lista_historia_clinica(request):
    historias_clinicas = HistoriaClinica.objects.all()
    return render(request, 'historia_clinica/lista.html', {'historias_clinicas': historias_clinicas})
#endregion







#region Antropometrico
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
    return render(request, 'dato_antropometrico/crear.html', {'formulario': formulario})

def lista_dato_antropometrico(request):
    datos_antropometricos = DatoAntropometrico.objects.all()
    return render(request, 'dato_antropometrico/lista.html', {'datos_antropometricos': datos_antropometricos})
#endregion







#region Cita
def registrar_cita(request):
    if request.method == 'POST':
        formulario = CitaForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, 'Cita creada exitosamente.')
            return redirect('crear_cita')
        else:
            messages.error(request, 'Por favor, llena todos los campos.')
    else:
        formulario = CitaForm()
    return render(request, 'cita/crear.html', {'formulario': formulario})

def lista_cita(request):
    citas = Cita.objects.all()
    return render(request, 'cita/lista.html', {'citas': citas})
#endregion







#region Incapacidad
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
    return render(request, 'certificado_incapacidad/crear.html', {'formulario': formulario})

def lista_certificado_incapacidad(request):
    certificados = CertificadoIncapacidad.objects.all()
    return render(request, 'certificado_incapacidad/lista.html', {'certificados': certificados})
#endregion







#region OrdenMedica
def registrar_orden_medica(request):
    if request.method == 'POST':
        formulario = OrdeneMedicaForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, 'Orden médica creada exitosamente.')
            return redirect('crear_orden_medica')
        else:
            messages.error(request, 'Por favor, llena todos los campos.')
    else:
        formulario = OrdeneMedicaForm()
    return render(request, 'orden_medica/crear.html', {'formulario': formulario})

def lista_orden_medica(request):
    ordenes = OrdenMedica.objects.all()
    return render(request, 'orden_medica/lista.html', {'ordenes': ordenes})
#endregion







#region Horario 
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

def lista_horario_medico(request):
    horarios = HorarioMedico.objects.all()
    return render(request, 'horario_medico/lista.html', {'horarios': horarios})

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

def eliminar_horario_medico(request, id):
    horario = get_object_or_404(HorarioMedico, id=id)
    horario.delete()
    messages.success(request, 'Horario médico eliminado exitosamente.')
    return redirect('lista_horario_medico')
#endregion










#region AGENDA


# Vista para mostrar el calendario con las citas disponibles
def calendario(request):
    return render(request, 'cita/calendario.html')

# Vista para obtener las citas disponibles del médico y mostrarlas en el calendario
def obtener_disponibilidad(request):
    eventos = []
    # Filtramos las disponibilidades de los médicos
    for disponibilidad in Disponibilidad.objects.all():
        evento = {
            'title': f'{disponibilidad.tipo_cita.capitalize()} disponible',
            'start': f'{disponibilidad.fecha}T{disponibilidad.hora_inicio}',
            'end': f'{disponibilidad.fecha}T{disponibilidad.hora_fin}',
            'color': 'yellow' if disponibilidad.tipo_cita == 'general' else 'blue',
        }
        eventos.append(evento)

    return JsonResponse(eventos, safe=False)

# Vista para verificar la disponibilidad al hacer clic en un día específico
def verificar_disponibilidad(request):
    fecha = request.GET.get('fecha')
    disponibilidad = Disponibilidad.objects.filter(fecha=fecha)
    if disponibilidad.exists():
        return JsonResponse({'disponible': True})
    return JsonResponse({'disponible': False})

# Vista para confirmar la cita después de la selección
def confirmar_cita(request):
    if request.method == 'POST':
        form = CitaForm(request.POST)
        if form.is_valid():
            cita = form.save(commit=False)
            cita.paciente = request.user.paciente  # Asumimos que el usuario es paciente
            cita.save()
            return render(request,'paciente/perfil.html')  # Redirige al perfil después de solicitar la cita
    else:
        form = CitaForm()
    return render(request, 'cita/confirmar_cita.html', {'form': form})

# Vista para que el médico registre su disponibilidad
def gestionar_disponibilidad(request):
    if request.method == 'POST':
        form = DisponibilidadForm(request.POST)
        if form.is_valid():
            disponibilidad = form.save(commit=False)
            disponibilidad.medico = request.user.medico  # Asumimos que el usuario es médico
            disponibilidad.save()
            return redirect('medico/perfil.html')  # Redirige al perfil del médico
    else:
        form = DisponibilidadForm()
    return render(request, 'cita/gestionar_disponibilidad.html', {'form': form})


#endregion






