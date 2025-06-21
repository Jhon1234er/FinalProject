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
            'username', 'password', 'first_name', 'last_name', 'email',
            'tipo_doc', 'num_doc', 'genero', 'rh', 'telefono',
            'fecha_nacimiento', 'tipo_poblacion', 'ocupacion', 'eps',
            'especialidad', 'numero_registro_profesional', 'licencia_certificacion', 'fecha_contratacion'
        ]
# endregion

# region Consulta
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
