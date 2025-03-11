from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField

# region Usuario Base
class Usuario(AbstractUser):
    OPCIONES_TIPODOC = [
        ('C.C', 'C.C'),
        ('T.I', 'T.I'),
        ('C.E', 'T.I'), 
    ]
    tipo_doc = models.CharField(max_length=20, choices=OPCIONES_TIPODOC)
    num_doc = models.CharField(max_length=10, unique=True)  
    OPCIONES_GENERO = [
        ('masculino', 'MASCULINO'),
        ('femenino', 'FEMENINO'),
        ('prefiero no decirlo', 'PREFIERO NO DECIRLO')
    ]
    genero = models.CharField(max_length=20, choices=OPCIONES_GENERO)
    rh = models.CharField(max_length=3)
    telefono = PhoneNumberField(null=True, blank=True)  # PhoneNumberField
    fecha_nacimiento = models.DateField(null=True, blank=True)
    tipo_poblacion = models.CharField(max_length=50)
    ocupacion = models.CharField(max_length=20)
    eps = models.CharField(max_length=20)

    def __str__(self):
        return self.username

#endregion


# region  Paciente
class Paciente(Usuario):
    OPCIONES_REGIMEN = [
        ('subcidiado', 'SUBCIDIADO'),
        ('contributivo', 'CONTRIBUTIVO'),
        ('otro', 'OTRO')
    ]
    regimen = models.CharField(max_length=30, choices=OPCIONES_REGIMEN )
    numero_seguro_social = models.CharField(max_length=15, unique=True)
#endregion


#region  Consulta
class Consulta(models.Model):
    tratamiento = models.TextField(max_length=200)
    diagnostico = models.TextField(max_length=200)
    motivo_consulta = models.TextField(max_length=200)
    fecha_consulta = models.DateField(null=False) 
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='consultas')
#endregion


#region  PerfilPaciente
class PerfilPaciente(models.Model):
    tratamiento = models.TextField(max_length=200, null=True)
    opcion_vida_sexual = [
        ('activo', 'ACTIVO'),
        ('no activo', 'NO ACTIVO')
    ]
    vida_sexual = models.CharField(max_length=50, choices=opcion_vida_sexual)
    ciclo_mestrual = models.TextField(max_length=200, null=True)
    sustancias_psicotivas = models.BooleanField(default=False)  
    habitos_alimenticios = models.TextField(max_length=200, null=True)
    consumo_alcohol = models.BooleanField(default=False)  
    habito_sueño = models.TextField(max_length=200, null=True)
    antecedentes_personales = models.TextField(max_length=200, null=True)
    consulta = models.OneToOneField(Consulta, on_delete=models.CASCADE, related_name='perfiles')
#endregion


#region  Antecedente
class Antecedente(models.Model):
    descripcion = models.TextField(max_length=200, null=True)
    tipo_antecedente = models.TextField(max_length=200, null=False)
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='antecedentes')
#endregion


#region  Vacuna
class Vacuna(models.Model):
    nombre_vacuna = models.CharField(max_length=150, null=False)
    fecha_aplicacion = models.DateField(null=False)
    dosis = models.CharField(max_length=100, null=False)  
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='vacunas')
#endregion


#region  DatoQuirurgico
class DatoQuirurgico(models.Model):
    tipo_cirugia = models.CharField(max_length=150, null=False)
    fecha_cirugia = models.DateField(null=False)
    complicaciones = models.TextField(max_length=200, null=False)
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='datos_quirurgicos')
#endregion


#region  HistoriaClinicas
class HistoriaClinica(models.Model):
    ultima_atencion = models.DateField()  # Esto lo gestionará Django automáticamente
    tratamiento = models.TextField()
    notas = models.TextField()
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)

#endregion


#region  DatoAntropometrico
class DatoAntropometrico(models.Model):
    altura_decimal = models.DecimalField(max_digits=20, decimal_places=2)
    peso = models.DecimalField(max_digits=20, decimal_places=2)
    indice_masa_corporal = models.DecimalField(max_digits=20, decimal_places=2)
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='datos_antropometricos')
#endregion


#region ** Empleado**
class Empleado(Usuario):
    opciones_tipo_empleado = [
        ('Medico', 'Medico'),
        ('auxiliar', 'Auxiliar'),
        ('administrador', 'Administrador')
    ]
    tipo_empleado = models.CharField(max_length=20, null=False, choices=opciones_tipo_empleado)
    usuario=models.ForeignKey(Usuario, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.tipo_empleado
        
#endregion

#region ** Administrador**
class Administrador(Empleado):
    # Este  gestiona la contratación de empleados
    fecha_contratacion = models.DateField(null=False)   
    # Gestión de archivos
    hoja_vida = models.FileField(upload_to='hojas_vida/', null=True, blank=True)  # Almacena las hojas de vida
    usuario=models.ForeignKey(Usuario, on_delete=models.CASCADE)
    contrato = models.FileField(upload_to='contratos/', null=True, blank=True)  # Almacena los contratos
    # Método para agregar documentos de empleados
    def agregar_documentos(self, empleado, hoja_vida, contrato):
        empleado.hoja_vida = hoja_vida  
        empleado.contrato = contrato
        empleado.save()
        return empleado
    
    def __str__(self):
        return self.hoja_vida
#endregion

#region  Medicos
class Medico(Empleado):
    especialidad = models.CharField(max_length=50, null=False)
    numero_licencia = models.CharField(max_length=10, null=False, unique=True)
    citas_atender = models.IntegerField(default=0)
    usuario=models.ForeignKey(Usuario, on_delete=models.CASCADE)
  
    def __str__(self):
        return self.especialidad
#endregion


#region ** IT**
class IT(Empleado):
    usuario=models.ForeignKey(Usuario, on_delete=models.CASCADE)

#endregion


#region  HorarioMedico
class HorarioMedico(models.Model):
    OPCIONES_DIAS_SEMANA = [
        ('lunes', 'Lunes'),
        ('martes', 'Martes'),
        ('miercoles', 'Miercoles'),
        ('jueves', 'Jueves'),
        ('viernes', 'Viernes'),
        ('sabado', 'Sabado'),
        ('domingo', 'Domingo')
    ]
    dia_semana = models.CharField(max_length=10, null=False, choices=OPCIONES_DIAS_SEMANA)
    hora_inicio = models.TimeField(null=False)
    hora_fin = models.TimeField(null=False)
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE, related_name='medico_horario')
#endregion


#region  Citas
class Cita(models.Model):
    fecha_cita = models.DateField(null=False)
    hora_cita = models.TimeField(null=False)
    OPCIONES_ESTADO_CITA = [
        ('pendiente', 'Pendiente'),
        ('confirmada', 'Confirmada'),
        ('cancelada', 'Cancelada')
    ]
    estado_cita = models.CharField(max_length=10, null=False, choices=OPCIONES_ESTADO_CITA)
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE, related_name='medico_citas')
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='pacientes')
#endregion


#region  CertificadoIncapacidad
class CertificadoIncapacidad(models.Model):
    dias_incapacidad = models.CharField(max_length=2)
    motivo_incapacidad = models.CharField(max_length=255)
    fecha_emision = models.DateField(auto_now=True)
    cita = models.ForeignKey(Cita, on_delete=models.CASCADE, related_name='certificados')
#endregion


#region  RecetasMedicas
class RecetaMedica(models.Model):
    medicamento = models.CharField(max_length=100)
    concentracion = models.CharField(max_length=100)
    duracion = models.CharField(max_length=100)
    cantidad = models.CharField(max_length=100)
    via_administracion = models.CharField(max_length=20)
    diagnostico_principal = models.TextField(max_length=255)
    diagnostico_relacionados = models.TextField(max_length=255)
    intervalo = models.CharField(max_length=20)
    recomendaciones = models.CharField(max_length=255)
    indicaciones = models.CharField(max_length=255)
    fecha_medicado = models.DateField(auto_now=True)
    cita = models.ForeignKey(Cita, on_delete=models.CASCADE, related_name='recetas')
#endregion


#region  OrdenesMedicas
class OrdeneMedica(models.Model):
    especialidad_referido = models.CharField(max_length=255, blank=False)
    motivo = models.CharField(max_length=255)
    fecha_ordenado = models.DateField(auto_now=True)
    cita = models.ForeignKey(Cita, on_delete=models.CASCADE, related_name='ordenes')
#endregion