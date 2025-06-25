from django import forms
from Izelapp.models import *
from django.utils import timezone
from django.core.exceptions import ValidationError
from datetime import datetime, date, timedelta

DURACIONES = [
    (20, "20 minutos"),
    (30, "30 minutos"),
    (45, "45 minutos"),
    (60, "1 hora"),
]

DIAS_SEMANA = [
    ('0', 'Lunes'),
    ('1', 'Martes'),
    ('2', 'Miércoles'),
    ('3', 'Jueves'),
    ('4', 'Viernes'),
    ('5', 'Sábado'),
    ('6', 'Domingo'),
]
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
            'fecha_nacimiento': forms.DateInput(attrs={'class': 'datepicker', 'type': 'text'}),  # Añadir clase datepicker
            'telefono': forms.TextInput(attrs={'placeholder': 'Ingrese su número de teléfono', 'id': 'id_telefono'}),            
            'password': forms.PasswordInput(),
            'email': forms.EmailInput(attrs={'placeholder': 'Ingrese su correo electrónico'}),
            'tipo_doc': forms.Select(attrs={'class': 'select2'}),
            'genero': forms.Select(attrs={'class': 'select2'}),
            'rh':forms.Select(attrs={'class':'select2'})
        }

    tipo_doc = forms.ChoiceField(label='Tipo de documento', choices=[('', 'Selecciona una opción')] + Usuario.OPCIONES_TIPODOC, widget=forms.Select(attrs={'class': 'select2'}))
    genero = forms.ChoiceField(label='Género', choices=[('', 'Selecciona una opción')] + Usuario.GENERO_OPCIONES, widget=forms.Select(attrs={'class': 'select2'}))
    rh=forms.ChoiceField(label='RH',choices=[('', 'Selecciona una opción')] + Usuario.RH_OPCIONES, widget=forms.Select(attrs={'class': 'select2'}))
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
    
class ImagenUserForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['imagen']
        widgets = {
            'imagen' : forms.FileInput()
        }
    
    def validar_imagen(self):
        imagen= self.cleaned_data.get(imagen)
        if imagen:
            extension = os.path.splitext(imagen.name)[1].lower()
            if extension not in ['jpg','png','jpeg']:
                raise ValidationError('No se aceptan imagenes en este formato, debe anexarla en formato PNG/JPG/JPEG')
            if imagen.size > 102400:
                raise ValidationError('El tamaño de su imagen exede el limite asigano que es 100 KB')
        return imagen
    #endregion

# endregion

# region Paciente
class PacienteForm(forms.ModelForm):
    regimen = forms.ChoiceField(
        choices=[('', 'Selecciona una opción')] + Paciente.OPCIONES_REGIMEN
    )

    tipo_doc = forms.ChoiceField(
        label='Tipo de documento',
        choices=[('', 'Selecciona una opción')] + Usuario.OPCIONES_TIPODOC,
        widget=forms.Select(attrs={'class': 'select2'})
    )

    genero = forms.ChoiceField(
        label='Género',
        choices=[('', 'Selecciona una opción')] + Usuario.GENERO_OPCIONES,
        widget=forms.Select(attrs={'class': 'select2'})
    )

    rh = forms.ChoiceField(
        label='RH',
        choices=[('', 'Selecciona una opción')] + Usuario.RH_OPCIONES,
        widget=forms.Select(attrs={'class': 'select2'})
    )

    num_doc = forms.CharField(label='Número de documento')
    tipo_poblacion = forms.CharField(label='Tipo de población')
    username = forms.CharField(label='Nombre de Usuario')
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput())
    first_name = forms.CharField(label='Nombres')
    last_name = forms.CharField(label='Apellidos')
    email = forms.EmailField(label='Correo')

    class Meta:
        model = Paciente
        fields = [
            'username', 'password', 'first_name', 'last_name', 'email',
            'tipo_doc', 'num_doc', 'genero', 'rh', 'telefono',
            'fecha_nacimiento', 'tipo_poblacion', 'ocupacion', 'eps',
            'regimen'
        ]
        widgets = {
            'fecha_nacimiento': forms.DateInput(attrs={
                'class': 'datepicker1', 'type': 'text', 'placeholder': 'Selecciona tu fecha de nacimiento'
            }),
            'telefono': forms.TextInput(attrs={
                'placeholder': 'Ej. 3001234567',
                'id': 'id_telefono',
                'class': 'form-control'
            }),
            'password': forms.PasswordInput(),
            'email': forms.EmailInput(attrs={'placeholder': 'Ingrese su correo electrónico'}),
            'tipo_doc': forms.Select(attrs={'class': 'select2'}),
            'genero': forms.Select(attrs={'class': 'select2'}),
            'rh': forms.Select(attrs={'class': 'select2'}),
        }
        labels = {
            'num_doc': 'Número de documento',
            'username': 'Nombre de Usuario',
            'password': 'Contraseña',
            'first_name': 'Nombres',
            'last_name': 'Apellidos',
            'email': 'Correo',
            'telefono': 'Teléfono',
            'fecha_nacimiento': 'Fecha de nacimiento',
            'tipo_poblacion': 'Tipo de población',
            'ocupacion': 'Ocupación',
            'eps': 'EPS',
            'regimen': 'Régimen de afiliación',
            'tipo_doc': 'Tipo de documento',
            'genero': 'Género',
            'rh': 'RH'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.Select):
                field.widget.attrs.update({'class': 'select2'})

    def clean_fecha_nacimiento(self):
        fecha_nacimiento = self.cleaned_data['fecha_nacimiento']
        hoy = timezone.now().date()
        if fecha_nacimiento:
            if fecha_nacimiento > hoy:
                raise ValidationError("No es permitido ingresar una fecha futura")
            edad = hoy.year - fecha_nacimiento.year
            if (hoy.month, hoy.day) < (fecha_nacimiento.month, fecha_nacimiento.day):
                edad -= 1
            if edad < 18:
                raise ValidationError("Debes tener al menos 18 años.")
        return fecha_nacimiento
    
class PacienteUpdateForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = ['email', 'telefono', 'tipo_poblacion']

    email = forms.EmailField(label='Correo', required=True)
    telefono = forms.CharField(label='Teléfono', required=False)
    tipo_poblacion = forms.CharField(label='Tipo de Población', required=False)
# endregion

# region Administrador
class AdministradorForm(forms.ModelForm):
    centro_administracion = forms.ChoiceField(
        choices=[('', 'Selecciona una opción')] + Administrador.AREAS_MEDICAS
    )

    class Meta:
        model = Administrador
        fields = [
            'username', 'password', 'first_name', 'last_name', 'email',
            'tipo_doc', 'num_doc', 'genero', 'rh', 'telefono',
            'fecha_nacimiento', 'tipo_poblacion', 'ocupacion', 'eps',
            'rol_acceso', 'centro_administracion'
        ]
        widgets = {
            'fecha_nacimiento': forms.DateInput(attrs={
                'class': 'datepicker1',
                'type': 'text',
                'placeholder': 'Seleccione la fecha de nacimiento'
            }),
            'telefono': forms.TextInput(attrs={
                'placeholder': 'Ej. 3001234567',
                'id': 'telefono-input',
                'class': 'form-control'
            }),
            'password': forms.PasswordInput(),
            'email': forms.EmailInput(attrs={'placeholder': 'Ingrese su correo electrónico'}),
            'rol_acceso': forms.TextInput(attrs={'placeholder': 'Rol de acceso del administrador'}),
            'tipo_doc': forms.Select(attrs={'class': 'select2'}),
            'genero': forms.Select(attrs={'class': 'select2'}),
            'rh': forms.Select(attrs={'class': 'select2'}),
            'centro_administracion': forms.Select(attrs={'class': 'select2'}),
        }
        labels = {
            'username': 'Nombre de Usuario',
            'password': 'Contraseña',
            'first_name': 'Nombre',
            'last_name': 'Apellido',
            'email': 'Correo',
            'tipo_doc': 'Tipo de documento',
            'num_doc': 'Número de documento',
            'genero': 'Género',
            'rh': 'RH',
            'telefono': 'Teléfono',
            'fecha_nacimiento': 'Fecha de nacimiento',
            'tipo_poblacion': 'Tipo de población',
            'ocupacion': 'Ocupación',
            'eps': 'EPS',
            'rol_acceso': 'Rol de Acceso',
            'centro_administracion': 'Centro de Administración',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.Select):
                field.widget.attrs.update({'class': 'select2'})

    def clean_fecha_nacimiento(self):
        fecha_nacimiento = self.cleaned_data['fecha_nacimiento']
        if fecha_nacimiento:
            hoy = timezone.now().date()
            if fecha_nacimiento > hoy:
                raise ValidationError("No es permitido ingresar una fecha futura")

            edad = hoy.year - fecha_nacimiento.year
            if (hoy.month, hoy.day) < (fecha_nacimiento.month, fecha_nacimiento.day):
                edad -= 1
            if edad < 18:
                raise ValidationError("Debes ser mayor de 18 años para registrarte")
        return fecha_nacimiento
        

class AdministradorUpdateForm(forms.ModelForm):
    class Meta:
        model= Administrador
        fields = ['email', 'telefono', 'tipo_poblacion']
    email = forms.EmailField(label='Correo', required=True)
    telefono = forms.CharField(label='Teléfono', required=False)
    tipo_poblacion = forms.CharField(label='Tipo de Población', required=False)
# endregion

#region Medico

class MedicoForm(forms.ModelForm):
    especialidad = forms.ChoiceField(
        choices=[('', 'Selecciona una opción')] + Medico.ESPECIALIDADES
    )

    class Meta:
        model = Medico
        fields = [
            'username', 'password', 'first_name', 'last_name', 'email',
            'tipo_doc', 'num_doc', 'genero', 'rh', 'telefono', 'fecha_nacimiento',
            'tipo_poblacion', 'eps', 'ocupacion', 'especialidad',
            'numero_registro_profesional', 'licencia_certificacion',
            'fecha_contratacion'
        ]
        widgets = {
            'fecha_contratacion': forms.DateInput(attrs={
                'class': 'datepicker', 'placeholder': 'Fecha de contratación'
            }),
            'fecha_nacimiento': forms.DateInput(attrs={
                'class': 'datepicker1', 'placeholder': 'Fecha de nacimiento'
            }),
            'telefono': forms.TextInput(attrs={
                'placeholder': 'Ej. 3001234567',
                'id': 'telefono-input',
                'class': 'form-control'
            }),
        }
    num_doc = forms.CharField(label='Número de documento')
    tipo_doc = forms.ChoiceField(label='Tipo de documento',
        choices=[('', 'Selecciona una opción')] + Usuario.OPCIONES_TIPODOC,
        widget=forms.Select(attrs={'class': 'select2'})
    )
    eps = forms.CharField(label='EPS')
    genero = forms.ChoiceField(
        choices=[('', 'Selecciona una opción')] + Usuario.GENERO_OPCIONES,
        widget=forms.Select(attrs={'class': 'select2'})
    )
    rh = forms.ChoiceField(label='RH',
        choices=[('', 'Selecciona una opción')] + Usuario.RH_OPCIONES,
        widget=forms.Select(attrs={'class': 'select2'})
    )
    password = forms.CharField(label='Contraseña',widget=forms.PasswordInput())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if isinstance(field.widget, forms.Select):
                field.widget.attrs.update({'class': 'select2'})

    def clean_fecha_nacimiento(self):
        fecha_nacimiento = self.cleaned_data['fecha_nacimiento']
        if fecha_nacimiento:
            hoy = timezone.now().date()
            edad = hoy.year - fecha_nacimiento.year
            if (hoy.month, hoy.day) < (fecha_nacimiento.month, fecha_nacimiento.day):
                edad -= 1
            if edad < 18:
                raise ValidationError("Debes tener al menos 18 años.")
        return fecha_nacimiento

    def clean_fecha_contratacion(self):
        fecha_contratacion = self.cleaned_data.get('fecha_contratacion')
        hoy = timezone.now().date()

        if fecha_contratacion:
            if fecha_contratacion < hoy:
                raise ValidationError("La fecha de contratación debe ser hoy o posterior.")
        return fecha_contratacion

class MedicoUpdateForm(forms.ModelForm):
    class Meta:
        model = Medico
        fields = ['email', 'telefono', 'tipo_poblacion']

    email = forms.EmailField(label='Correo', required=True)
    telefono = forms.CharField(label='Teléfono', required=False)
    tipo_poblacion = forms.CharField(label='Tipo de Población', required=False)
#endregion

# region Consulta
class ConsultaForm(forms.ModelForm):
    diagnostico_principal = forms.ModelChoiceField(
        queryset=TablaReferenciaCIE10.objects.all(),
        empty_label="Seleccione un diagnóstico principal",
        widget=forms.Select(attrs={
            'class': 'form-control select2',
            'data-placeholder': 'Seleccione un diagnóstico principal'
        }),
        required=True
    )

    diagnostico_relacionado = forms.ModelChoiceField(
        queryset=TablaReferenciaCIE10.objects.all(),
        empty_label="Seleccione un diagnóstico relacionado",
        widget=forms.Select(attrs={
            'class': 'form-control select2',
            'data-placeholder': 'Seleccione un diagnóstico relacionado'
        }),
        required=False 
    )

    class Meta:
        model = Consulta
        fields = [
            'especialidad',
            'tratamiento',
            'diagnostico_principal',
            'diagnostico_relacionado',
            'motivo_consulta',
        ]
        widgets = {
            'especialidad': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Especialidad'
            }),
            'tratamiento': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Descripción del tratamiento'
            }),
            'motivo_consulta': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Motivo de la consulta'
            }),
        }
        labels = {
            'especialidad': 'Especialidad',
            'tratamiento': 'Tratamiento',
            'diagnostico_principal': 'Diagnóstico Principal',
            'diagnostico_relacionado': 'Diagnóstico Relacionado',
            'motivo_consulta': 'Motivo de Consulta',
            'medico': 'Médico'
        }

#endregion

# region PerfilPaciente
class PerfilPacienteForm(forms.ModelForm):
    vida_sexual = forms.ChoiceField(choices=[('', 'Selecciona una opción')] + PerfilPaciente.OPCIONES_VIDA_SEXUAL)

    class Meta:
        model = PerfilPaciente
        fields = ['tratamiento', 'vida_sexual', 'ciclo_mestrual', 'sustancias_psicotivas','habitos_alimenticios', 'consumo_alcohol', 'habito_sueño','antecedentes_personales', 'consulta'
        ]
        widgets = {
            'tratamiento': forms.Textarea(attrs={'rows': 4}),
            'ciclo_mestrual': forms.Textarea(attrs={'rows': 4}),
            'habitos_alimenticios': forms.Textarea(attrs={'rows': 4}),
            'antecedentes_personales': forms.Textarea(attrs={'rows': 4}),
        }
# endregion

# region HorarioMedico
class HorarioMedicoForm(forms.ModelForm):
    dia_semana = forms.ChoiceField(choices=[('', 'Selecciona una opción')] + HorarioMedico.OPCIONES_DIAS_SEMANA)

    class Meta:
        model = HorarioMedico
        fields = ['medico', 'dia_semana', 'hora_inicio', 'hora_fin'
        ]
# endregion

# region Cita
class CitaForm(forms.ModelForm):
    estado_cita = forms.ChoiceField(choices=[('', 'Selecciona una opción')] + Cita.OPCIONES_ESTADO_CITA)

    class Meta:
        model = Cita
        fields = ['fecha_cita', 'hora_cita', 'estado_cita', 'especialidad','medico', 'paciente', 'disponibilidad'
        ]
# endregion

# region CertificadoIncapacidad
class CertificadoIncapacidadForm(forms.ModelForm):
    class Meta:
        model = CertificadoIncapacidad
        fields = ['medico', 'paciente', 'dias_incapacidad', 'motivo_incapacidad','fecha_inicio', 'fecha_fin', 'diagnostico_principal', 'diagnostico_relacionado', 'observaciones'
        ]
# endregion


#region RecetaMedica 

class RecetaMedicaForm(forms.ModelForm):
    class Meta:
        model = RecetaMedica
        fields = [
            'medicamento', 'concentracion', 'duracion', 'cantidad', 'via_administracion', 'diagnostico_principal','diagnostico_relacionado', 'intervalo', 'recomendaciones', 'indicaciones','fecha_medicado',
        ]
    widgets = {
        'medicamento': forms.TextInput(attrs={'class': 'form-control'}),
        'concentracion': forms.TextInput(attrs={'class': 'form-control'}),
        'duracion': forms.TextInput(attrs={'class': 'form-control'}),
        'cantidad': forms.TextInput(attrs={'class': 'form-control'}),
        'via_administracion': forms.TextInput(attrs={'class': 'form-control'}),
        'intervalo': forms.TextInput(attrs={'class': 'form-control'}),
        'recomendaciones': forms.TextInput(attrs={'class': 'form-control'}),
        'indicaciones': forms.TextInput(attrs={'class': 'form-control'}),
        'fecha_medicado': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),  # Solo lectura
    }

    diagnostico_principal = forms.ModelChoiceField(
        queryset=TablaReferenciaCIE10.objects.all(),
        empty_label="Seleccione un diagnóstico principal",
        widget=forms.Select(attrs={
            'class': 'form-control select2',
            'data-placeholder': 'Seleccione un diagnóstico principal'
        }),
        required=True
    )

    diagnostico_relacionado = forms.ModelChoiceField(
        queryset=TablaReferenciaCIE10.objects.all(),
        empty_label="Seleccione un diagnóstico relacionado",
        widget=forms.Select(attrs={
            'class': 'form-control select2',
            'data-placeholder': 'Seleccione un diagnóstico relacionado'
        }),
        required=False  # Puede ser opcional
    )
#endregion


# region OrdenMedica
class OrdenMedicaForm(forms.ModelForm):
    estado = forms.ChoiceField(choices=[('', 'Selecciona una opción')] + OrdenMedica.ESTADO_CITA)

    class Meta:
        model = OrdenMedica
        fields = ['cups', 'medico', 'paciente', 'especialidad_referido', 'cantidad','diagnostico_principal', 'diagnostico_relacionado', 'motivo','fecha_ordenado', 'vigencia', 'estado'
        ]
# endregion

# region Disponibilidad
class DisponibilidadForm(forms.ModelForm):
    tipo_cita = forms.ChoiceField(choices=[('', 'Selecciona una opción')] + Disponibilidad.TIPO_CITA)
    estado = forms.ChoiceField(choices=[('', 'Selecciona una opción')] + Disponibilidad.ESTADOS)

    class Meta:
        model = Disponibilidad
        fields = ['medico', 'fecha', 'hora_inicio', 'hora_fin', 'tipo_cita', 'estado', 'max_pacientes', 'duracion'
        ]
# endregion

# region Antecedente
class AntecedenteForm(forms.ModelForm):
    class Meta:
        model = Antecedente
        fields = ['descripcion', 'tipo_antecedente'
        ]
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 4}),
        }
# endregion

# region Vacuna
class VacunaForm(forms.ModelForm):
    class Meta:
        model = Vacuna
        fields = ['nombre_vacuna', 'fecha_aplicacion', 'dosis'
        ]
        widgets = {
            'fecha_aplicacion': forms.DateInput(attrs={'type': 'date'}),
            'dosis': forms.TextInput(attrs={'placeholder': 'Dosis de la vacuna'}),
        }
# endregion

# region DatoQuirurgico
class DatoQuirurgicoForm(forms.ModelForm):
    class Meta:
        model = DatoQuirurgico
        fields = ['tipo_cirugia', 'fecha_cirugia', 'complicaciones'
        ]
        widgets = {
            'fecha_cirugia': forms.DateInput(attrs={'type': 'date'}),
            'complicaciones': forms.Textarea(attrs={'rows': 4}),
        }
# endregion

# region HistoriaClinica
class RegistroClinicoForm(forms.ModelForm):
    class Meta:
        model = HistoriaClinica
        fields = ['ultima_atencion', 'tratamiento', 'notas'
        ]
        widgets = {
            'ultima_atencion': forms.DateInput(attrs={'type': 'date', 'readonly': 'readonly'}),  # Solo lectura
            'tratamiento': forms.Textarea(attrs={'rows': 4}),
            'notas': forms.Textarea(attrs={'rows': 4}),
        }
# endregion

# region DatoAntropometrico
class DatoAntropometricoForm(forms.ModelForm):
    class Meta:
        model = DatoAntropometrico
        fields = ['altura_decimal', 'peso', 'indice_masa_corporal'
        ]
        widgets = {
            'altura_decimal': forms.NumberInput(attrs={'placeholder': 'Altura en metros'}),
            'peso': forms.NumberInput(attrs={'placeholder': 'Peso en kg'}),
            'indice_masa_corporal': forms.NumberInput(attrs={'placeholder': 'Índice de masa corporal'}),
        }
# endregion

#region HorarioMedico 
class HorarioMedicoForm(forms.ModelForm):
    class Meta:
        model = HorarioMedico
        fields = ['dia_semana', 'hora_inicio', 'hora_fin', 'medico'
                  ]
        widgets = {
            'hora_inicio': forms.TimeInput(attrs={'type': 'time'}),
            'hora_fin': forms.TimeInput(attrs={'type': 'time'}),
            'dia_semana': forms.Select(attrs={'class': 'form-control'}),
        }
#endregion

#region Cita
class CitaForm(forms.ModelForm):
    class Meta:
        model = Cita
        fields = ['fecha_cita', 'hora_cita',  'especialidad', 'medico', 'paciente'
        ]
        widgets = {
            'fecha_cita': forms.DateInput(attrs={'type': 'date','readonly': 'readonly' }),
            'hora_cita': forms.TimeInput(attrs={'type': 'time','readonly': 'readonly'}),
            'estado_cita': forms.Select(attrs={'class': 'form-control','readonly': 'readonly'}),
            'medico': forms.Select (attrs={'class': 'from-control','readonly': 'readonly'}),
            'paciente':forms.Select(attrs={'class': 'from-control','readonly': 'readonly'}),
        }
#endregion

#region Disponibilidad

class GenerarDisponibilidadForm(forms.Form):
    medicos = forms.ModelMultipleChoiceField(
        queryset=Medico.objects.all(),
        widget=forms.MultipleHiddenInput(),  # Lo manejamos por JavaScript
        required=False
    )
    fecha_inicio = forms.DateField(widget=forms.DateInput(attrs={'class': 'datepicker form-control'}))
    fecha_fin = forms.DateField(widget=forms.DateInput(attrs={'class': 'datepicker form-control'}))
    dias = forms.MultipleChoiceField(
        choices=DIAS_SEMANA,
        widget=forms.CheckboxSelectMultiple,
        label='Días de la semana'
    )
    hora_inicio = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}))
    hora_fin = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}))
    duracion = forms.ChoiceField(
        choices=DURACIONES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

#endregion


#region OrdeneMedica
class OrdenMedicaForm(forms.ModelForm):
    diagnostico_principal = forms.ModelChoiceField(
        queryset=TablaReferenciaCIE10.objects.all(),
        empty_label="Seleccione un diagnóstico principal",
        widget=forms.Select(attrs={
            'class': 'form-control select2',
            'data-placeholder': 'Seleccione un diagnóstico principal'
        }),
        required=True
    )

    diagnostico_relacionado = forms.ModelChoiceField(
        queryset=TablaReferenciaCIE10.objects.all(),
        empty_label="Seleccione un diagnóstico relacionado",
        widget=forms.Select(attrs={
            'class': 'form-control select2',
            'data-placeholder': 'Seleccione un diagnóstico relacionado'
        }),
        required=False  # Puede ser opcional
    )

    class Meta:
        model = OrdenMedica
        fields = ['cups', 'especialidad_referido', 'cantidad', 'diagnostico_principal','diagnostico_relacionado', 'motivo', 'vigencia'
        ]
        widgets = {
            'cups': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Código CUPS'}),
            'especialidad_referido': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Especialidad a la que remite'}),
            'cantidad': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Cantidad'}),
            'diagnostico_principal': forms.Textarea(attrs={'class': 'form-control','placeholder':'No especificado'}),
            'diagnostico_relacionado': forms.Textarea(attrs={'class': 'form-control','placeholder':'No especificado'}),            
            'motivo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Motivo de la orden'}),
            'fecha_ordenado': forms.DateInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'vigencia': forms.SelectDateWidget(attrs={'class': 'form-control'}, years=range(2025, 2026)),
        }
#endregion



# region Incapacidad Medica
class CertificadoIncapacidadForm(forms.ModelForm):
    diagnostico_principal = forms.ModelChoiceField(
        queryset=TablaReferenciaCIE10.objects.all(),
        empty_label="Seleccione un diagnóstico principal",
        widget=forms.Select(attrs={
            'class': 'form-control select2',
            'data-placeholder': 'Seleccione un diagnóstico principal'
        }),
        required=True
    )

    diagnostico_relacionado = forms.ModelChoiceField(
        queryset=TablaReferenciaCIE10.objects.all(),
        empty_label="Seleccione un diagnóstico relacionado",
        widget=forms.Select(attrs={
            'class': 'form-control select2',
            'data-placeholder': 'Seleccione un diagnóstico relacionado'
        }),
        required=False  # Puede ser opcional
    )


    class Meta:
        model = CertificadoIncapacidad
        fields = ['dias_incapacidad', 'motivo_incapacidad', 'fecha_inicio', 'fecha_fin', 
                  'diagnostico_principal', 'diagnostico_relacionado', 'observaciones'
                  ]
        widgets = {
            'dias_incapacidad': forms.TextInput(attrs={'class': 'form-control'}),
            'motivo_incapacidad': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha_inicio': forms.SelectDateWidget(attrs={'class': 'form-control'}, years=range(2025, 2026)),
            'fecha_fin': forms.SelectDateWidget(attrs={'class': 'form-control'}, years=range(2025, 2026)),
            'observaciones': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Observaciones'})
        }
#endregion

