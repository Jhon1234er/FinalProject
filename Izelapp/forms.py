from django import forms
from Izelapp.models import (
    Usuario, Paciente, Administrador, Medico, PerfilPaciente,
    HorarioMedico, Cita, OrdenMedica, Disponibilidad, Antecedente,
    Vacuna, DatoQuirurgico, HistoriaClinica, CertificadoIncapacidad,
    RecetaMedica, Consulta, DatoAntropometrico
)
from django.core.exceptions import ValidationError

# region Usuario
class UsuarioForm(forms.ModelForm):
    tipo_doc = forms.ChoiceField(choices=[('', 'Selecciona una opción')] + Usuario.OPCIONES_TIPODOC)
    genero = forms.ChoiceField(choices=[('', 'Selecciona una opción')] + Usuario.GENERO_OPCIONES)
    rh = forms.ChoiceField(choices=[('', 'Selecciona una opción')] + Usuario.RH_OPCIONES)

    class Meta:
        model = Usuario
        fields = [
            'username', 'password', 'first_name', 'last_name', 'email',
            'tipo_doc', 'num_doc', 'genero', 'rh', 'telefono',
            'fecha_nacimiento', 'tipo_poblacion', 'ocupacion', 'eps', 'imagen'
        ]
        widgets = {
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date'}),
            'password': forms.PasswordInput(),
            'email': forms.EmailInput(),
        }

class ImagenUserForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['imagen']

    def clean_imagen(self):
        imagen = self.cleaned_data.get('imagen')
        if imagen and imagen.size > 2 * 1024 * 1024:
            raise ValidationError("La imagen no puede superar los 2MB.")
        return imagen
# endregion

# region Paciente
class PacienteForm(forms.ModelForm):
    regimen = forms.ChoiceField(choices=[('', 'Selecciona una opción')] + Paciente.OPCIONES_REGIMEN)

    class Meta:
        model = Paciente
        fields = [
            'username', 'password', 'first_name', 'last_name', 'email',
            'tipo_doc', 'num_doc', 'genero', 'rh', 'telefono',
            'fecha_nacimiento', 'tipo_poblacion', 'ocupacion', 'eps',
            'regimen'
        ]
# endregion

# region Administrador
class AdministradorForm(forms.ModelForm):
    centro_administracion = forms.ChoiceField(choices=[('', 'Selecciona una opción')] + Administrador.AREAS_MEDICAS)

    class Meta:
        model = Administrador
        fields = [
            'username', 'password', 'first_name', 'last_name', 'email',
            'tipo_doc', 'num_doc', 'genero', 'rh', 'telefono',
            'fecha_nacimiento', 'tipo_poblacion', 'ocupacion', 'eps',
            'rol_acceso', 'centro_administracion'
        ]
# endregion

# region Medico
class MedicoForm(forms.ModelForm):
    especialidad = forms.ChoiceField(choices=[('', 'Selecciona una opción')] + Medico.ESPECIALIDADES)

    class Meta:
        model = Medico
        fields = [
            # USUARIO
            'username',
            'password',
            'first_name', 
            'last_name', 
            'email',
            'tipo_doc',
            'num_doc',
            'genero',
            'rh',
            'telefono',
            'fecha_nacimiento',
            'tipo_poblacion',
            'eps',
            'ocupacion',
            # MEDICO
            'especialidad',
            'numero_registro_profesional',
            'licencia_certificacion',
            'fecha_contratacion' 
        ]
        widgets = {
            'fecha_contratacion': forms.DateInput(attrs={'class':'datepicker','type':'text','placeholder':'Ingrese la fecha de contratacion del medico'}),
            'fecha_nacimiento': forms.DateInput(attrs={'class':'datepicker','type': 'text','placeholder':'Ingrese la fecha de nacimiento del medico'}),
            'especialidad': forms.Select(attrs={'class': 'select2'}),
            'numero_registro_profesional': forms.TextInput(attrs={'placeholder': 'Número de registro profesional'}),
        }
    
    tipo_doc = forms.ChoiceField(label='Tipo de documento', choices=[('', 'Selecciona una opción')] + Usuario.OPCIONES_TIPODOC, widget=forms.Select(attrs={'class': 'select2'}))
    genero = forms.ChoiceField(label='Género', choices=[('', 'Selecciona una opción')] + Usuario.OPCIONES_GENERO, widget=forms.Select(attrs={'class': 'select2'}))
    rh=forms.ChoiceField(label='RH',choices=[('', 'Selecciona una opción')] + Usuario.OPCIONES_RH, widget=forms.Select(attrs={'class': 'select2'}))
    num_doc = forms.CharField(label='Número de documento')
    tipo_poblacion = forms.CharField(label='Tipo de población')
    username = forms.CharField(label='Nombre de Usuario')
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput())
    first_name = forms.CharField(label='Primer Nombre')
    last_name = forms.CharField(label='Apellido')
    email = forms.CharField(label='Correo')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.Select):
                field.widget.attrs.update({'class': 'select2'})

    def clean_fecha_nacimiento(self):
        fecha_nacimiento = self.cleaned_data['fecha_nacimiento']
        if fecha_nacimiento:
            if fecha_nacimiento > timezone.now().date():
                raise ValidationError("NO SE PERMITEN FECHAS FUTURAS")
            edad = timezone.now().date().year - fecha_nacimiento.year
            if (timezone.now().date().month, timezone.now().date().day) < (fecha_nacimiento.month, fecha_nacimiento.day):
                edad -= 1 
            if edad < 18:
                raise ValidationError("DEBES SER MAYOR A 18 AÑOS")
        return fecha_nacimiento

    def clean_fecha_contratacion(self):
        fecha_contratacion = self.cleaned_data['fecha_contratacion']
        if fecha_contratacion:
            # Verifica que la fecha de contratación no sea una fecha pasada
            if fecha_contratacion < timezone.now().date():
                raise ValidationError("La fecha de contratación no puede ser una fecha pasada.")
        return fecha_contratacion
#endregion









#region Auxiliar
class AuxiliarForm(forms.ModelForm):
    class Meta:
        model = Auxiliar
        fields = [
            # USUARIO
            'username',
            'password',
            'tipo_doc',
            'num_doc',
            'genero',
            'rh',
            'telefono',
            'fecha_nacimiento',
            'tipo_poblacion',
            'eps',
            'ocupacion',
            # AUXILIAR
            'departamento',  
            'supervisor',  
        ]
        widgets = {
            'fecha_nacimiento': forms.DateInput(attrs={'class': 'datepicker', 'type': 'text','placeholder':'Seleccione la fecha de nacimiento'}),
            'departamento': forms.TextInput(attrs={'placeholder': 'Área de trabajo del auxiliar'}),
            'supervisor': forms.TextInput(attrs={'placeholder': 'Nombre del supervisor'}),
        }
        
    tipo_doc = forms.ChoiceField(label='Tipo de documento', choices=[('', 'Selecciona una opción')] + Usuario.OPCIONES_TIPODOC, widget=forms.Select(attrs={'class': 'select2'}))
    genero = forms.ChoiceField(label='Género', choices=[('', 'Selecciona una opción')] + Usuario.OPCIONES_GENERO, widget=forms.Select(attrs={'class': 'select2'}))
    rh=forms.ChoiceField(label='RH',choices=[('', 'Selecciona una opción')] + Usuario.OPCIONES_RH, widget=forms.Select(attrs={'class': 'select2'}))
    num_doc = forms.CharField(label='Número de documento')
    tipo_poblacion = forms.CharField(label='Tipo de población')
    username = forms.CharField(label='Nombre de Usuario')
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput())
    first_name = forms.CharField(label='Primer Nombre')
    last_name = forms.CharField(label='Apellido')
    email = forms.CharField(label='Correo')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.Select):
                field.widget.attrs.update({'class': 'select2'})


    def clean_fecha_nacimiento(self):
        fecha_nacimiento = self.cleaned_data['fecha_nacimiento']
        if fecha_nacimiento:
            # Verifica que la fecha no sea una fecha futura
            if fecha_nacimiento > timezone.now().date():
                raise ValidationError("ERROR DE INGRESO DE FECHA DE NACIMIENTO")
            
            # Verifica que la edad sea mayor a 18 años
            edad = timezone.now().date().year - fecha_nacimiento.year
            if (timezone.now().date().month, timezone.now().date().day) < (fecha_nacimiento.month, fecha_nacimiento.day):
                edad -= 1 
            if edad < 18:
                raise ValidationError("LA EDAD INGRESADA DEBE SER MAYOR A 18")
        return fecha_nacimiento




class ConsultaForm(forms.ModelForm):
    class Meta:
        model = Consulta
        fields = [
            'especialidad', 'tratamiento', 'diagnostico_principal', 'diagnostico_relacionado',
            'motivo_consulta', 'medico', 'paciente'
        ]
# endregion

# region PerfilPaciente
class PerfilPacienteForm(forms.ModelForm):
    vida_sexual = forms.ChoiceField(choices=[('', 'Selecciona una opción')] + PerfilPaciente.OPCIONES_VIDA_SEXUAL)

    class Meta:
        model = PerfilPaciente
        fields = [
            'tratamiento', 'vida_sexual', 'ciclo_mestrual', 'sustancias_psicotivas',
            'habitos_alimenticios', 'consumo_alcohol', 'habito_sueño',
            'antecedentes_personales', 'consulta'
        ]
# endregion

# region HorarioMedico
class HorarioMedicoForm(forms.ModelForm):
    dia_semana = forms.ChoiceField(choices=[('', 'Selecciona una opción')] + HorarioMedico.OPCIONES_DIAS_SEMANA)

    class Meta:
        model = HorarioMedico
        fields = [
            'medico', 'dia_semana', 'hora_inicio', 'hora_fin'
        ]
# endregion

# region Cita
class CitaForm(forms.ModelForm):
    estado_cita = forms.ChoiceField(choices=[('', 'Selecciona una opción')] + Cita.OPCIONES_ESTADO_CITA)

    class Meta:
        model = Cita
        fields = [
            'fecha_cita', 'hora_cita', 'estado_cita', 'especialidad',
            'medico', 'paciente', 'disponibilidad'
        ]
# endregion

# region CertificadoIncapacidad
class CertificadoIncapacidadForm(forms.ModelForm):
    class Meta:
        model = CertificadoIncapacidad
        fields = [
            'medico', 'paciente', 'dias_incapacidad', 'motivo_incapacidad',
            'fecha_inicio', 'fecha_fin', 'diagnostico_principal', 'diagnostico_relacionado', 'observaciones'
        ]
# endregion

# region RecetaMedica
class RecetaMedicaForm(forms.ModelForm):
    class Meta:
        model = RecetaMedica
        fields = [
            'medico', 'paciente', 'medicamento', 'concentracion', 'duracion',
            'cantidad', 'via_administracion', 'diagnostico_principal'
        ]
# endregion

# region OrdenMedica
class OrdenMedicaForm(forms.ModelForm):
    estado = forms.ChoiceField(choices=[('', 'Selecciona una opción')] + OrdenMedica.ESTADO_CITA)

    class Meta:
        model = OrdenMedica
        fields = [
            'cups', 'medico', 'paciente', 'especialidad_referido', 'cantidad',
            'diagnostico_principal', 'diagnostico_relacionado', 'motivo',
            'fecha_ordenado', 'vigencia', 'estado'
        ]
# endregion

# region Disponibilidad
class DisponibilidadForm(forms.ModelForm):
    tipo_cita = forms.ChoiceField(choices=[('', 'Selecciona una opción')] + Disponibilidad.TIPO_CITA)
    estado = forms.ChoiceField(choices=[('', 'Selecciona una opción')] + Disponibilidad.ESTADOS)

    class Meta:
        model = Disponibilidad
        fields = [
            'medico', 'fecha', 'hora_inicio', 'hora_fin', 'tipo_cita', 'estado', 'max_pacientes', 'duracion'
        ]
# endregion

# region Antecedente
class AntecedenteForm(forms.ModelForm):
    class Meta:
        model = Antecedente
        fields = [
            'descripcion', 'tipo_antecedente', 'paciente'
        ]
# endregion

# region Vacuna
class VacunaForm(forms.ModelForm):
    class Meta:
        model = Vacuna
        fields = [
            'nombre_vacuna', 'fecha_aplicacion', 'dosis', 'paciente'
        ]
# endregion

# region DatoQuirurgico
class DatoQuirurgicoForm(forms.ModelForm):
    class Meta:
        model = DatoQuirurgico
        fields = [
            'tipo_cirugia', 'fecha_cirugia', 'complicaciones', 'paciente', 'medico'
        ]
# endregion

# region HistoriaClinica
class HistoriaClinicaForm(forms.ModelForm):
    class Meta:
        model = HistoriaClinica
        fields = [
            'ultima_atencion', 'tratamiento', 'notas', 'paciente'
        ]
# endregion

# region DatoAntropometrico
class DatoAntropometricoForm(forms.ModelForm):
    class Meta:
        model = DatoAntropometrico
        fields = [
            'altura_decimal', 'peso', 'indice_masa_corporal', 'paciente', 'medico'
        ]
# endregion
