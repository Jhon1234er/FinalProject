from django import forms
from Izelapp.models import *
from django.utils import timezone
from django.core.exceptions import ValidationError


#region Usuario
class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['username',
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
                  'ocupacion', 
                  'eps'
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







#region Paciente
class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = [
            #USUARIO
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
            'ocupacion',
            'eps', 
            #PACIENTE
            'regimen', 
            'numero_seguro_social'
            ]
        widgets = {
            'numero_seguro_social': forms.TextInput(attrs={'placeholder': 'Número de Seguro Social'}),
            'fecha_nacimiento': forms.DateInput(attrs={'class': 'datepicker', 'type': 'text'}),  # Añadir clase datepicker
            'telefono': forms.TextInput(attrs={'placeholder': 'Ingrese su número de teléfono', 'id': 'id_telefono'}),            
            'password': forms.PasswordInput(),
            'email': forms.EmailInput(attrs={'placeholder': 'Ingrese su correo electrónico'}),
            'tipo_doc': forms.Select(attrs={'class': 'select2'}),
            'genero': forms.Select(attrs={'class': 'select2'}),
            'rh':forms.Select(attrs={'class':'select2'})
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
#endregion






#region Administrador
class AdministradorForm(forms.ModelForm):
    class Meta:
        model = Administrador
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
            'ocupacion',
            'eps',
            # ADMINISTRADOR
            'rol_acceso',
            'centro_administracion',
        ]
        widgets = {
            'fecha_nacimiento': forms.DateInput(attrs={'class': 'datepicker', 'type': 'text','placeholder':'Seleccione la fecha de nacimiento'}),
            'rol_acceso': forms.TextInput(attrs={'placeholder': 'Rol de acceso del administrador'}),
            'centro_administracion': forms.TextInput(attrs={'placeholder': 'Centro de administración'}),
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
                edad -= 1  # Ajuste por no haber cumplido aún el cumpleaños este año
            if edad < 18:
                raise ValidationError("DEBES SER MAYOR A 18 AÑOS")
        return fecha_nacimiento
#endregion








#region TI
class TIForm(forms.ModelForm):
    class Meta:
        model = TI
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
            'ocupacion',
            'eps',
            #TI
            'is_staff',
            'is_superuser'
            ]
        widgets = {
            'fecha_nacimiento': forms.DateInput(attrs={'class': 'datepicker', 'type': 'text','placeholder':'Seleccione la fecha de nacimiento'}),
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


    def save(self, commit=True):
        it_instance = super().save(commit=False)
        usuario = it_instance.usuario

        usuario.is_staff = self.cleaned_data['is_staff']
        usuario.is_superuser = self.cleaned_data['is_superuser']
        if commit:
            usuario.save()  
            it_instance.save() 

        return it_instance
#endregion    







#region Medico
class MedicoForm(forms.ModelForm):
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
            'especialidad': forms.TextInput(attrs={'placeholder': 'Especialidad del médico'}),
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
            'especialidad',
            'tratamiento',
            'diagnostico_principal',
            'diagnostico_relacionado',
            'motivo_consulta',
        ]

        # Personalización de los widgets
        widgets = {
            'especialidad': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Especialidad'}),
            'tratamiento': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Descripción del tratamiento'}),
            'diagnostico_principal': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Diagnóstico principal'}),
            'diagnostico_relacionado': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Diagnóstico relacionado'}),
            'motivo_consulta': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Motivo de la consulta'}),
        }

        # Etiquetas personalizadas
        labels = {
            'especialidad': 'Especialidad',
            'tratamiento': 'Tratamiento',
            'diagnostico_principal': 'Diagnóstico Principal',
            'diagnostico_relacionado': 'Diagnóstico Relacionado',
            'motivo_consulta': 'Motivo de Consulta',
            'medico': 'Médico'
        }

#endregion








#region PerfilPaciente
class PerfilPacienteForm(forms.ModelForm):
    class Meta:
        model = PerfilPaciente
        fields = ['tratamiento', 
                  'vida_sexual', 
                  'ciclo_mestrual', 
                  'sustancias_psicotivas', 
                  'habitos_alimenticios', 
                  'consumo_alcohol', 
                  'habito_sueño', 
                  'antecedentes_personales', 
                  'consulta'
                  ]
        widgets = {
            'tratamiento': forms.Textarea(attrs={'rows': 4}),
            'ciclo_mestrual': forms.Textarea(attrs={'rows': 4}),
            'habitos_alimenticios': forms.Textarea(attrs={'rows': 4}),
            'antecedentes_personales': forms.Textarea(attrs={'rows': 4}),
        }
#endregion








#region Antecedente
class AntecedenteForm(forms.ModelForm):
    class Meta:
        model = Antecedente
        fields = ['descripcion',
                  'tipo_antecedente'
                  ]
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 4}),
        }
#endregion








#region Vacuna
class VacunaForm(forms.ModelForm):
    class Meta:
        model = Vacuna
        fields = ['nombre_vacuna',
                  'fecha_aplicacion', 
                  'dosis'
                  ]
        widgets = {
            'fecha_aplicacion': forms.DateInput(attrs={'type': 'date'}),
            'dosis': forms.TextInput(attrs={'placeholder': 'Dosis de la vacuna'}),
        }
#endregion








#region DatoQuirurgico 
class DatoQuirurgicoForm(forms.ModelForm):
    class Meta:
        model = DatoQuirurgico
        fields = ['tipo_cirugia', 
                  'fecha_cirugia', 
                  'complicaciones'
                  ]
        widgets = {
            'fecha_cirugia': forms.DateInput(attrs={'type': 'date'}),
            'complicaciones': forms.Textarea(attrs={'rows': 4}),
        }
#endregion







#region HistoriaClinica
class HistoriaClinicaForm(forms.ModelForm):
    class Meta:
        model = HistoriaClinica
        fields = ['ultima_atencion',
                  'tratamiento',
                  'notas',
                  'paciente'
                  ]
        widgets = {
            'ultima_atencion': forms.DateInput(attrs={'type': 'date', 'readonly': 'readonly'}),  # Solo lectura
            'tratamiento': forms.Textarea(attrs={'rows': 4}),
            'notas': forms.Textarea(attrs={'rows': 4}),
        }








#region DatoAntropometrico 
class DatoAntropometricoForm(forms.ModelForm):
    class Meta:
        model = DatoAntropometrico
        fields = ['altura_decimal', 
                  'peso', 
                  'indice_masa_corporal', 
                  ]
        widgets = {
            'altura_decimal': forms.NumberInput(attrs={'placeholder': 'Altura en metros'}),
            'peso': forms.NumberInput(attrs={'placeholder': 'Peso en kg'}),
            'indice_masa_corporal': forms.NumberInput(attrs={'placeholder': 'Índice de masa corporal'}),
        }
#endregion







#region HorarioMedico 
class HorarioMedicoForm(forms.ModelForm):
    class Meta:
        model = HorarioMedico
        fields = ['dia_semana', 
                  'hora_inicio', 
                  'hora_fin', 
                  'medico'
                  ]
        widgets = {
            'hora_inicio': forms.TimeInput(attrs={'type': 'time'}),
            'hora_fin': forms.TimeInput(attrs={'type': 'time'}),
            'dia_semana': forms.Select(attrs={'class': 'form-control'}),
        }
#endregion



#region AgendaMedico
class AgendaMedicaForm(forms.ModelForm):
    class Meta:
        model = AgendaMedica
        fields = ['medico', 'hora', 'paciente', 'motivo']
        widgets = {
            'hora': forms.TimeInput(attrs={'type': 'time'}),
        }
#endregion



#region Cita
# forms.py
class CitaForm(forms.ModelForm):
    class Meta:
        model = Cita
        fields = ['fecha_cita',
                  'hora_cita', 
                  'especialidad', 
                  'medico', 
                  'paciente']

        widgets = {
            'fecha_cita': forms.DateInput(attrs={'type': 'date','readonly': 'readonly' }),
            'hora_cita': forms.TimeInput(attrs={'type': 'time','readonly': 'readonly'}),
            'estado_cita': forms.Select(attrs={'class': 'form-control','readonly': 'readonly'}),
            'medico': forms.Select (attrs={'class': 'from-control','readonly': 'readonly'}),
            'paciente':forms.Select(attrs={'class': 'from-control','readonly': 'readonly'}),
        }
#endregion















#region RecetaMedica 

class RecetaMedicaForm(forms.ModelForm):
    class Meta:
        model = RecetaMedica
        fields = [
            'medicamento',
            'concentracion',
            'duracion',
            'cantidad',
            'via_administracion',
            'diagnostico_principal',
            'diagnostico_relacionado',
            'intervalo',
            'recomendaciones',
            'indicaciones',
            'fecha_medicado',
        ]

    widgets = {
        'medicamento': forms.TextInput(attrs={'class': 'form-control'}),
        'concentracion': forms.TextInput(attrs={'class': 'form-control'}),
        'duracion': forms.TextInput(attrs={'class': 'form-control'}),
        'cantidad': forms.TextInput(attrs={'class': 'form-control'}),
        'via_administracion': forms.TextInput(attrs={'class': 'form-control'}),
        'diagnostico_principal': forms.Textarea(attrs={'class': 'form-control','placeholder':'No especificado'}),
        'diagnostico_relacionado': forms.Textarea(attrs={'class': 'form-control','placeholder':'No especificado'}),
        'intervalo': forms.TextInput(attrs={'class': 'form-control'}),
        'recomendaciones': forms.TextInput(attrs={'class': 'form-control'}),
        'indicaciones': forms.TextInput(attrs={'class': 'form-control'}),
        'fecha_medicado': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),  # Solo lectura
    }

#endregion







#region OrdeneMedica
class OrdenMedicaForm(forms.ModelForm):
    class Meta:
        model = OrdenMedica
        fields = ['cups', 'especialidad_referido', 'cantidad', 'diagnostico_principal','diagnostico_relacionado', 'motivo', 'vigencia']
        
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
    class Meta:
        model = CertificadoIncapacidad
        fields = ['dias_incapacidad', 'motivo_incapacidad', 'fecha_inicio', 'fecha_fin', 
                  'diagnostico_principal', 'diagnostico_relacionado', 'observaciones']
        
        widgets = {
            'dias_incapacidad': forms.TextInput(attrs={'class': 'form-control'}),
            'motivo_incapacidad': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha_inicio': forms.SelectDateWidget(attrs={'class': 'form-control'}, years=range(2025, 2026)),
            'fecha_fin': forms.SelectDateWidget(attrs={'class': 'form-control'}, years=range(2025, 2026)),
            'diagnostico_principal': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Diagnóstico principal'}),
            'diagnostico_relacionado': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Diagnósticos relacionados'}),
            'observaciones': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Observaciones'})
        }
#endregion