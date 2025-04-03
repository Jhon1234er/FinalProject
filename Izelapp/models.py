from django.db import models
import os, json
import logging
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField

# Destinar una carpeta en el sistema de archivos para subir documentos
def user_directory_path(instance, filename):
    return f"usuario/{instance.id}_{filename}"


# Configuración del logger
logger = logging.getLogger(__name__)





# region Usuario 
class Usuario(AbstractUser):
    OPCIONES_TIPODOC = [
        ('CC', 'Cédula de Ciudadanía'),
        ('TI', 'Tarjeta de identidad'),
        ('CE', 'Cédula de Extranjería')
    ]
    tipo_doc = models.CharField(max_length=20, choices=OPCIONES_TIPODOC)
    num_doc = models.CharField(max_length=10, unique=True)  
    email = models.EmailField(unique=True, blank=False)
    OPCIONES_GENERO = [
        ('masculino', 'MASCULINO'),
        ('femenino', 'FEMENINO'),
        ('prefiero no decirlo', 'PREFIERO NO DECIRLO')
    ]
    genero = models.CharField(max_length=20, choices=OPCIONES_GENERO)
    OPCIONES_RH=[('A+','A+'),
                ('A-','A-'),
                ('B+','B+'),
                ('B-','B-'),
                ('AB+','AB+'),
                ('AB-','AB-'),
                ('O+','O+'),
                ('O-','O-')
    ]
    rh = models.CharField(max_length=3,choices=OPCIONES_RH)
    telefono = PhoneNumberField(null=True, blank=True)  # PhoneNumberField
    fecha_nacimiento = models.DateField(null=True, blank=True)
    tipo_poblacion = models.CharField(max_length=50)
    ocupacion = models.CharField(max_length=20)
    eps = models.CharField(max_length=20)
    imagen = models.ImageField(upload_to=user_directory_path, blank=True, null=True, verbose_name='Imagen')

    def __str__(self):
        return self.username
    
    # Eliminar la imagen del servidor si el usuario se borra
    def delete(self,*args,**kwargs):
        if self.imagen and self.imagen.name:
            self.eliminar_imagen()
        super().delete(*args,**kwargs)

    def eliminar_imagen(self):
        try:
            # Se comprueba si hay una imagen y si hay ruta de acceso a ella en MEDIA_ROOT
            if self.imagen and self.imagen.name and os.path.isfile(self.imagen.path):
                os.remove(self.imagen.path)
                logger.info(f"Imagen eliminada correctamente: {self.imagen.path}")
            else:
                logger.warning(f"La imagen no existe o no tiene un nombre válido: {self.imagen.path}")
        except Exception as e:
            logger.error(f"Error al eliminar la imagen {self.imagen.path}: {e}")


#endregion






# region Paciente
class Paciente(Usuario):
    OPCIONES_REGIMEN = [
        ('subcidiado', 'SUBCIDIADO'),
        ('contributivo', 'CONTRIBUTIVO'),
        ('otro', 'OTRO')
    ]
    regimen = models.CharField(max_length=30, choices=OPCIONES_REGIMEN )
    numero_seguro_social = models.CharField(max_length=15, unique=True)
#endregion






#region Administrador
class Administrador(Usuario):
    rol_acceso = models.CharField(max_length=100)  
    centro_administracion = models.CharField(max_length=255)
    permisos = models.JSONField()  


    def save(self, *args, **kwargs):
        # Asigna los permisos automáticamente al crear un administrador
        if not self.permisos:
            self.permisos = {
                "ODONTOLOGIA": {
                    "medico": {"ver_pacientes": True, "editar_pacientes": True, "ver_historia_clinica": True, "realizar_tratamientos": True},
                    "auxiliar": {"ver_pacientes": True, "realizar_tratamientos": False},
                    "administrador": {"ver_pacientes": True, "editar_pacientes": True, "ver_historia_clinica": True, "gestion_usuarios": True}
                },
                "CIRUGIA": {
                    "medico": {"ver_pacientes": True, "realizar_cirugia": True, "ver_historia_clinica": True},
                    "auxiliar": {"ver_pacientes": True, "realizar_cirugia": False},
                    "administrador": {"ver_pacientes": True, "realizar_cirugia": True, "ver_historia_clinica": True, "gestion_usuarios": True}
                },
                "GENERAL": {
                    "medico": {"ver_pacientes": True, "ver_historia_clinica": True},
                    "auxiliar": {"ver_pacientes": True, "ver_historia_clinica": False},
                    "administrador": {"ver_pacientes": True, "ver_historia_clinica": True, "gestion_usuarios": True}
                },
                "RAYOS_X": {
                    "medico": {"ver_pacientes": True, "ver_imagenes": True, "realizar_imagenes": True},
                    "auxiliar": {"ver_pacientes": True, "ver_imagenes": False},
                    "administrador": {"ver_pacientes": True, "ver_imagenes": True, "realizar_imagenes": True, "gestion_usuarios": True}
                }
            }
        super().save(*args, **kwargs)
#endregion




#region Medicos
class Medico(Usuario):
    especialidad = models.CharField(max_length=100)
    numero_registro_profesional = models.CharField(max_length=50)
    licencia_certificacion = models.BooleanField(default=False)
    fecha_contratacion = models.DateField()

    def __str__(self):
        return f"{self.first_name}"
#endregion





#region Auxiliar
class Auxiliar(Usuario):
    departamento = models.CharField(max_length=100)
    supervisor = models.CharField(max_length=255)
#endregion






#region TI
class TI(Usuario):
    is_staff = models.BooleanField(default=False),
#endregion






#region Consulta
class Consulta(models.Model):
    tratamiento = models.TextField(max_length=200)
    diagnostico = models.TextField(max_length=200)
    motivo_consulta = models.TextField(max_length=200)
    fecha_consulta = models.DateField(null=False) 
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='consultas')
#endregion






#region PerfilPaciente
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







#region Antecedente
class Antecedente(models.Model):
    descripcion = models.TextField(max_length=200, null=True)
    tipo_antecedente = models.TextField(max_length=200, null=False)
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='antecedentes')
#endregion






#region Vacuna
class Vacuna(models.Model):
    nombre_vacuna = models.CharField(max_length=150, null=False)
    fecha_aplicacion = models.DateField(null=False)
    dosis = models.CharField(max_length=100, null=False)  
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='vacunas')
#endregion






#region DatoQuirurgico
class DatoQuirurgico(models.Model):
    tipo_cirugia = models.CharField(max_length=150, null=False)
    fecha_cirugia = models.DateField(null=False)
    complicaciones = models.TextField(max_length=200, null=False)
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='datos_quirurgicos')
#endregion






#region HistoriaClinicas
class HistoriaClinica(models.Model):
    ultima_atencion = models.DateField()  # Esto lo gestionará Django automáticamente
    tratamiento = models.TextField()
    notas = models.TextField()
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
#endregion







#region DatoAntropometrico
class DatoAntropometrico(models.Model):
    altura_decimal = models.DecimalField(max_digits=20, decimal_places=2)
    peso = models.DecimalField(max_digits=20, decimal_places=2)
    indice_masa_corporal = models.DecimalField(max_digits=20, decimal_places=2)
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='datos_antropometricos')
#endregion






#region Contratacion
class Contratacion(models.Model):
    # Este  gestiona la contratación de empleados
    fecha_contratacion = models.DateField(null=False)   
    # Gestión de archivos
    hoja_vida = models.FileField(upload_to='hojas_vida/', null=True, blank=True)  # Almacena las hojas de vida
    contrato = models.FileField(upload_to='contratos/', null=True, blank=True)  # Almacena los contratos
    # Método para agregar documentos de empleados
    def agregar_documentos(self, empleado, hoja_vida, contrato):
        empleado.hoja_vida = hoja_vida  
        empleado.contrato = contrato
        empleado.save()
        return empleado
#endregion





#region Horario medico
class HorarioMedico(models.Model):
    OPCIONES_DIAS_SEMANA = [
        ('lunes', 'Lunes'),
        ('martes', 'Martes'),
        ('miercoles', 'Miércoles'),
        ('jueves', 'Jueves'),
        ('viernes', 'Viernes'),
        ('sabado', 'Sábado'),
        ('domingo', 'Domingo')
    ]

    medico = models.ForeignKey(Medico, on_delete=models.CASCADE)
    dia_semana = models.CharField(max_length=10, choices=OPCIONES_DIAS_SEMANA, default='lunes')  # No es necesario null=False cuando usas choices
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
#endregion





#region Citas
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






#region CertificadoIncapacidad
class CertificadoIncapacidad(models.Model):
    dias_incapacidad = models.CharField(max_length=2)
    motivo_incapacidad = models.CharField(max_length=255)
    fecha_emision = models.DateField(auto_now=True)
    cita = models.ForeignKey(Cita, on_delete=models.CASCADE, related_name='certificados')
#endregion






#region RecetasMedicas
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
class OrdenMedica(models.Model):
    especialidad_referido = models.CharField(max_length=255, blank=False)
    motivo = models.CharField(max_length=255)
    fecha_ordenado = models.DateField(auto_now=True)
    cita = models.ForeignKey(Cita, on_delete=models.CASCADE, related_name='ordenes')
#endregion









#region Disponibilidad 
class Disponibilidad(models.Model):
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE)
    fecha = models.DateField()
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    tipo_cita = models.CharField(max_length=50, choices=[('general', 'General'), ('odontologia', 'Odontología')])

    def __str__(self):
        return f"{self.medico} - {self.fecha} de {self.hora_inicio} a {self.hora_fin}"
    
#endregion