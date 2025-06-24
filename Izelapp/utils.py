from django.core.mail import send_mail
from django.conf import settings

def enviar_correo_recuperacion(usuario):
    asunto = 'Recuperación de contraseña - Izel'
    mensaje = f"""
Hola {usuario.first_name},

Has solicitado restablecer tu contraseña.

Haz clic en el siguiente enlace para crear una nueva contraseña:
http://localhost:8000/restablecer/{usuario.pk}/

Si no hiciste esta solicitud, ignora este correo.

Equipo Izel.
"""
    remitente = settings.DEFAULT_FROM_EMAIL
    destinatario = [usuario.email]

    send_mail(asunto, mensaje, remitente, destinatario, fail_silently=False)
