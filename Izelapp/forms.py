from django import forms
from .models import *

# **Usuario Form**
class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['username', 'password', 'tipo_doc', 'num_doc', 'genero', 'rh', 'telefono', 'fecha_nacimiento', 'tipo_poblacion', 'ocupacion', 'eps']
        widgets = {
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date'}),
            'telefono': forms.TextInput(attrs={'placeholder': 'Ingrese su número de teléfono'}),
            'password': forms.PasswordInput(),
        }

# **Paciente Form**
class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = ['regimen', 'numero_seguro_social']
        widgets = {
            'numero_seguro_social': forms.TextInput(attrs={'placeholder': 'Número de Seguro Social'}),
        }

# **Consulta Form**
class ConsultaForm(forms.ModelForm):
    class Meta:
        model = Consulta
        fields = ['tratamiento', 'diagnostico', 'motivo_consulta', 'fecha_consulta', 'paciente']
        widgets = {
            'fecha_consulta': forms.SelectDateWidget(),
            'tratamiento': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Descripción del tratamiento'}),
            'diagnostico': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Diagnóstico del paciente'}),
            'motivo_consulta': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Motivo de la consulta'}),
        }

# **PerfilPaciente Form**
class PerfilPacienteForm(forms.ModelForm):
    class Meta:
        model = PerfilPaciente
        fields = ['tratamiento', 'vida_sexual', 'ciclo_mestrual', 'sustancias_psicotivas', 'habitos_alimenticios', 'consumo_alcohol', 'habito_sueño', 'antecedentes_personales', 'consulta']
        widgets = {
            'tratamiento': forms.Textarea(attrs={'rows': 4}),
            'ciclo_mestrual': forms.Textarea(attrs={'rows': 4}),
            'habitos_alimenticios': forms.Textarea(attrs={'rows': 4}),
            'antecedentes_personales': forms.Textarea(attrs={'rows': 4}),
        }

# **Antecedente Form**
class AntecedenteForm(forms.ModelForm):
    class Meta:
        model = Antecedente
        fields = ['descripcion', 'tipo_antecedente', 'paciente']
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 4}),
        }

# **Vacuna Form**
class VacunaForm(forms.ModelForm):
    class Meta:
        model = Vacuna
        fields = ['nombre_vacuna', 'fecha_aplicacion', 'dosis', 'paciente']
        widgets = {
            'fecha_aplicacion': forms.DateInput(attrs={'type': 'date'}),
            'dosis': forms.TextInput(attrs={'placeholder': 'Dosis de la vacuna'}),
        }

# **DatoQuirurgico Form**
class DatoQuirurgicoForm(forms.ModelForm):
    class Meta:
        model = DatoQuirurgico
        fields = ['tipo_cirugia', 'fecha_cirugia', 'complicaciones', 'paciente']
        widgets = {
            'fecha_cirugia': forms.DateInput(attrs={'type': 'date'}),
            'complicaciones': forms.Textarea(attrs={'rows': 4}),
        }

# **HistoriaClinica Form**
class HistoriaClinicaForm(forms.ModelForm):
    class Meta:
        model = HistoriaClinica
        fields = ['ultima_atencion', 'tratamiento', 'notas', 'paciente']
        widgets = {
            'ultima_atencion': forms.DateInput(attrs={'type': 'date', 'readonly': 'readonly'}),  # Solo lectura
            'tratamiento': forms.Textarea(attrs={'rows': 4}),
            'notas': forms.Textarea(attrs={'rows': 4}),
        }


# **DatoAntropometrico Form**
class DatoAntropometricoForm(forms.ModelForm):
    class Meta:
        model = DatoAntropometrico
        fields = ['altura_decimal', 'peso', 'indice_masa_corporal', 'paciente']
        widgets = {
            'altura_decimal': forms.NumberInput(attrs={'placeholder': 'Altura en metros'}),
            'peso': forms.NumberInput(attrs={'placeholder': 'Peso en kg'}),
            'indice_masa_corporal': forms.NumberInput(attrs={'placeholder': 'Índice de masa corporal'}),
        }

# **Empleado Form**
class EmpleadoForm(forms.ModelForm):
    class Meta:
        model = Empleado
        fields = ['tipo_empleado']
        widgets = {
            'tipo_empleado': forms.Select(attrs={'class': 'form-control'}),
        }

# **Administrador Form**
class AdministradorForm(forms.ModelForm):
    class Meta:
        model = Administrador
        fields = ['fecha_contratacion', 'hoja_vida', 'contrato']
        widgets = {
            'fecha_contratacion': forms.DateInput(attrs={'type': 'date'}),
            'hoja_vida': forms.ClearableFileInput(),
            'contrato': forms.ClearableFileInput(),
        }

# **IT Form**
class ITForm(forms.ModelForm):
    class Meta:
        model = IT
        exclude = ['cuenta_creada']  # Excluye el campo de la creación automática
        fields = ['cuenta_creada', 'cuenta_activa', 'permisos', 'acciones']
        widgets = {
            'permisos': forms.Textarea(attrs={'rows': 4}),
            'acciones': forms.Textarea(attrs={'rows': 4}),
        }

# **Medicos Form**
class MedicosForm(forms.ModelForm):
    class Meta:
        model = Medico
        fields = ['especialidad', 'numero_licencia', 'citas_atender']
        widgets = {
            'especialidad': forms.TextInput(attrs={'placeholder': 'Especialidad del médico'}),
            'numero_licencia': forms.TextInput(attrs={'placeholder': 'Número de licencia'}),
            'citas_atender': forms.NumberInput(attrs={'placeholder': 'Número de citas a atender'}),
        }

# **HorarioMedico Form**
class HorarioMedicoForm(forms.ModelForm):
    class Meta:
        model = HorarioMedico
        fields = ['dia_semana', 'hora_inicio', 'hora_fin', 'medico']
        widgets = {
            'hora_inicio': forms.TimeInput(attrs={'type': 'time'}),
            'hora_fin': forms.TimeInput(attrs={'type': 'time'}),
            'dia_semana': forms.Select(attrs={'class': 'form-control'}),
        }

# **Cita Form**
class CitaForm(forms.ModelForm):
    class Meta:
        model = Cita
        fields = ['fecha_cita', 'hora_cita', 'estado_cita', 'medico', 'paciente']
        widgets = {
            'fecha_cita': forms.DateInput(attrs={'type': 'date'}),
            'hora_cita': forms.TimeInput(attrs={'type': 'time'}),
            'estado_cita': forms.Select(attrs={'class': 'form-control'}),
        }

# **CertificadoIncapacidad Form**
class CertificadoIncapacidadForm(forms.ModelForm):
    class Meta:
        model = CertificadoIncapacidad
        fields = ['dias_incapacidad', 'motivo_incapacidad', 'cita']
        widgets = {
            'fecha_emision': forms.DateInput(attrs={'type': 'date'}),
            'motivo_incapacidad': forms.Textarea(attrs={'rows': 4}),
        }

# **RecetaMedica Form**
class RecetaMedicaForm(forms.ModelForm):
    class Meta:
        model = RecetaMedica
        fields = ['medicamento', 
                  'concentracion', 'duracion', 'cantidad', 'via_administracion', 'diagnostico_principal', 'diagnostico_relacionados', 'intervalo', 'recomendaciones', 'indicaciones',  'cita']
        widgets = {
            'fecha_medicado': forms.DateInput(attrs={'type': 'date','readonly': 'readonly'}),
            'medicamento': forms.TextInput(attrs={'placeholder': 'Nombre del medicamento'}),
            'concentracion': forms.TextInput(attrs={'placeholder': 'Concentración del medicamento'}),
            'cantidad': forms.NumberInput(attrs={'placeholder': 'Cantidad prescrita'}),
            'intervalo': forms.TextInput(attrs={'placeholder': 'Intervalo de administración'}),
            'recomendaciones': forms.Textarea(attrs={'rows': 4}),
            'indicaciones': forms.Textarea(attrs={'rows': 4}),
        }

# **OrdeneMedica Form**
class OrdeneMedicaForm(forms.ModelForm):
    class Meta:
        model = OrdeneMedica
        fields = ['especialidad_referido', 'motivo', 'cita']
        widgets = {
            'fecha_ordenado': forms.DateInput(attrs={'type': 'date','readonly': 'readonly'}),
            'motivo': forms.Textarea(attrs={'rows': 4}),
            'especialidad_referido': forms.TextInput(attrs={'placeholder': 'Especialidad a la que se refiere'}),
        }
