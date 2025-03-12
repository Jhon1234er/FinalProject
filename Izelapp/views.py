from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from Izelapp.forms import *
from Izelapp.models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash

#region **Home**
def home(request):
    return render(request, 'home.html')

#endregion

# region **Usuario **

def registrar_usuario(request):
    if request.method == 'POST':
        formulario = UsuarioForm(request.POST)
        if formulario.is_valid():
            usuario = formulario.save(commit=False)
            usuario.set_password(formulario.cleaned_data['password'])  # Encripta la contraseña
            usuario.save()
            messages.success(request, 'Usuario creado exitosamente.')
            return redirect('registrar_usuario')
        else:
            print(formulario.errors)  # Muestra los errores del formulario en la consola
            messages.error(request, 'Hay algunos errores en el registro. Vuelva a intentar...')
    else:
        formulario = UsuarioForm()
    return render(request, 'usuario/insertar.html', {'formulario': formulario})

def lista_usuario(request):
    usuarios = Usuario.objects.all()
    return render(request, 'usuario/lista.html', {'usuarios': usuarios})

def eliminar_usuario(request, id):
    usuario = get_object_or_404(Usuario, id=id)
    usuario.delete()
    messages.success(request, 'Usuario eliminado exitosamente.')
    return redirect('listar_usuarios')

# Vista para login
def login_usuario(request):
    if request.method == 'POST':
        # Obtener datos del formulario
        username_recibido = request.POST.get('username')
        password_recibido = request.POST.get('password')

        if not username_recibido or not password_recibido:
            return render(request, 'usuario/login.html', {'mensaje_error': 'Por favor, complete todos los campos.'})

        # Autenticación estándar
        usuario = authenticate(request, username=username_recibido, password=password_recibido)
        
        if usuario is not None:
            # Si las credenciales son correctas, realizar login
            login(request, usuario)
            
            # Verificar si el usuario tiene algún perfil (médico, cliente, usuario común)
            if hasattr(usuario, 'medico'):  # Si el usuario tiene relación con médico
                return render('medico:perfil')  # Redirigir al perfil del médico
            elif hasattr(usuario, 'cliente'):  # Si el usuario tiene relación con cliente
                return render('cliente:perfil')  # Redirigir al perfil del cliente
            else:
                return render(request,'usuario/perfil.html',{'tipo_usuario':'Bienvenido usuario'})  # Redirigir al perfil de usuario común
        else:
            # Si las credenciales son incorrectas
            return render(request, 'usuario/login.html', {'mensaje_error': 'Credenciales incorrectas, intente de nuevo.'})
    
    return render(request, 'usuario/login.html')  # Si no es POST, simplemente renderizar el formulario de login

@login_required
def ver_perfil_usuario(request):
    usuario = request.user  # Obtener el usuario logueado
    return render(request, 'usuario/perfil.html', {'usuario': usuario})

@login_required
def detallar_usuario(request):
    usuario = request.user  # Obtener el usuario logueado
    return render(request, 'usuario/detallar.html', {'usuario': usuario})

@login_required
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


# Vista para logout
def logout_usuario(request):
    logout(request)
    messages.success(request, 'Has cerrado sesión exitosamente.')
    return redirect('home')  # Redirigir al home después de hacer logout

#endregion

# region **Paciente **

def crear_paciente(request):
    if request.method == 'POST':
        formulario = PacienteForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, 'Paciente creado exitosamente.')
            return redirect('crear_paciente')
        else:
            messages.error(request, 'Por favor, llena todos los campos.')
    else:
        formulario = PacienteForm()
    return render(request, 'paciente/crear.html', {'formulario': formulario})

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

# region**Consulta **

def crear_consulta(request):
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

#region **PerfilPaciente **

def crear_perfil_paciente(request):
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

# region**Vacuna **

def crear_vacuna(request):
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

# **Eliminar ** (Aplica para varios modelos)

def eliminar_vacuna(request, id):
    vacuna = get_object_or_404(Vacuna, id=id)
    vacuna.delete()
    messages.success(request, 'Vacuna eliminada exitosamente.')
    return redirect('listar_vacuna')

#endregion

#region **RecetaMedica **

def crear_receta_medica(request):
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

# **Eliminar  for other models (like OrdeneMedica)**

def eliminar_receta_medica(request, id):
    receta = get_object_or_404(RecetaMedica, id=id)
    receta.delete()
    messages.success(request, 'Receta médica eliminada exitosamente.')
    return redirect('listar_receta_medica')

#endregion

# region **Antecedentes**
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

# region **Quirurgico**

def crear_dato_quirurgico(request):
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

# region **Historial**

def crear_historia_clinica(request):
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

# region **Antropometrico**

def crear_dato_antropometrico(request):
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

# region **Cita**

def crear_cita(request):
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

# region **Incapacidad**

def crear_certificado_incapacidad(request):
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

# region **OrdenMedica**

def crear_orden_medica(request):
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
    ordenes = OrdeneMedica.objects.all()
    return render(request, 'orden_medica/lista.html', {'ordenes': ordenes})

#endregion

#region **Empleados**
def crear_empleado(request):
    usuarios = Usuario.objects.all()  # Obtener todos los usuarios
    formulario_empleado = EmpleadoForm()
    formulario_administrador = AdministradorForm()
    formulario_it = ITForm()
    formulario_medico = MedicosForm()

    if request.method == 'POST':
        tipo_empleado = request.POST.get('tipo_empleado')
        
        if tipo_empleado == 'empleado':
            formulario = EmpleadoForm(request.POST)
            if formulario.is_valid():
                empleado = formulario.save(commit=False)
                usuario_id = request.POST.get('usuario')
                usuario = Usuario.objects.get(id=usuario_id)
                empleado.usuario = usuario
                empleado.save()
                return redirect('listar_empleado')
        elif tipo_empleado == 'administrador':
            formulario = AdministradorForm(request.POST)
            if formulario.is_valid():
                administrador = formulario.save(commit=False)
                usuario_id = request.POST.get('usuario')
                usuario = Usuario.objects.get(id=usuario_id)
                administrador.usuario = usuario
                administrador.save()
                return redirect('listar_administrador')
        elif tipo_empleado == 'it':
            formulario = ITForm(request.POST)
            if formulario.is_valid():
                formulario.save()
                messages.success(request, 'IT creado exitosamente.')
                return redirect('listar_it')
        elif tipo_empleado == 'medico':
            formulario = MedicosForm(request.POST)
            if formulario.is_valid():
                medico = formulario.save(commit=False)
                usuario_id = request.POST.get('usuario')
                usuario = Usuario.objects.get(id=usuario_id)
                medico.usuario = usuario
                medico.save()
                return redirect('listar_medico')
        else:
            messages.error(request, 'Por favor, selecciona un tipo de empleado válido.')

    return render(request, 'empleado/insertar.html', {
        'formulario_empleado': formulario_empleado,
        'formulario_administrador': formulario_administrador,
        'formulario_it': formulario_it,
        'formulario_medico': formulario_medico,
        'usuarios': usuarios
    })


def lista_empleado(request):
    empleados = Empleado.objects.all()
    return render(request, 'empleado/lista.html', {'empleados': empleados})

def actualizar_empleado(request, id):
    empleado = get_object_or_404(Empleado, id=id)
    if request.method == 'POST':
        formulario = EmpleadoForm(request.POST, instance=empleado)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, 'Empleado actualizado exitosamente.')
            return redirect('listar_empleado')
        else:
            messages.error(request, 'Por favor, revisa los campos.')
    else:
        formulario = EmpleadoForm(instance=empleado)
    return render(request, 'empleado/actualizar.html', {'formulario': formulario})

def eliminar_empleado(request, id):
    empleado = get_object_or_404(Empleado, id=id)
    empleado.delete()
    messages.success(request, 'Empleado eliminado exitosamente.')
    return redirect('listar_empleado')

#endregion

#region ** Administrador **
def crear_administrador(request):
    usuarios = Usuario.objects.all()  # Obtener todos los usuarios
    if request.method == 'POST':
        formulario = AdministradorForm(request.POST)
        if formulario.is_valid():
            administrador = formulario.save(commit=False)
            # Asignar el usuario seleccionado al nuevo administrador
            usuario_id = request.POST.get('usuario')
            usuario = Usuario.objects.get(id=usuario_id)
            administrador.usuario = usuario
            administrador.save()
            return redirect('listar_administrador')  # Redirigir a la lista de administradores
    else:
        formulario = AdministradorForm()

    return render(request, 'administrador/insertar.html', {
        'formulario': formulario,
        'usuarios': usuarios
    })

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

#region ** IT **
def crear_it(request):
    if request.method == 'POST':
        formulario = ITForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, 'IT creado exitosamente.')
            return redirect('registrar_it')
        else:
            messages.error(request, 'Por favor, llena todos los campos.')
    else:
        formulario = ITForm()

    return render(request, 'ti/insertar.html', {'formulario': formulario})

def lista_it(request):
    its = IT.objects.all()
    return render(request, 'ti/lista.html', {'its': its})

def actualizar_it(request, id):
    it = get_object_or_404(IT, id=id)
    if request.method == 'POST':
        formulario = ITForm(request.POST, instance=it)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, 'IT actualizado exitosamente.')
            return redirect('listar_it')
        else:
            messages.error(request, 'Por favor, revisa los campos.')
    else:
        formulario = ITForm(instance=it)

    return render(request, 'ti/actualizar.html', {'formulario': formulario})

def eliminar_it(request, id):
    it = get_object_or_404(IT, id=id)
    it.delete()
    messages.success(request, 'IT eliminado exitosamente.')
    return redirect('listar_it')

#endregion

#region ** Medicos **
def crear_medico(request):
    usuarios = Usuario.objects.all()  # Obtener todos los usuarios
    if request.method == 'POST':
        formulario = MedicosForm(request.POST)
        if formulario.is_valid():
            medico = formulario.save(commit=False)
            # Asignar el usuario seleccionado al nuevo médico
            usuario_id = request.POST.get('usuario')
            usuario = Usuario.objects.get(id=usuario_id)
            medico.usuario = usuario
            medico.save()
            return redirect('listar_medico')  # Redirigir a la lista de médicos
    else:
        formulario = MedicosForm()

    return render(request, 'medico/insertar.html', {
        'formulario': formulario,
        'usuarios': usuarios
    })

def lista_medico(request):
    medicos = Medico.objects.all()
    return render(request, 'medico/lista.html', {'medicos': medicos})

def actualizar_medico(request, id):
    medico = get_object_or_404(Medico, id=id)
    if request.method == 'POST':
        formulario = MedicosForm(request.POST, instance=medico)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, 'Médico actualizado exitosamente.')
            return redirect('listar_medico')
        else:
            messages.error(request, 'Por favor, revisa los campos.')
    else:
        formulario = MedicosForm(instance=medico)
    return render(request, 'medico/actualizar.html', {'formulario': formulario})

def eliminar_medico(request, id):
    medico = get_object_or_404(Medico, id=id)
    medico.delete()
    messages.success(request, 'Médico eliminado exitosamente.')
    return redirect('listar_medico')


#endregion

#region ** Horario **
def crear_horario_medico(request):
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




# CON ESTA INFORMACION REALIZA LOS HTML DE 
# *Usuario : ACTUALIZAR, INSERTAR, LISTA, DETALLAR, lOGIN , PERFIL
# *Vacuna
# *Receta Medica
# *Perfil Paciente
# *Paciente
# *Historia Clinica
# *Dato Antropometrico 

# TAMBIEN 

# *Base 
# *Home 
#  estos seran los principales las demas heredaran el encabezado y el footer 