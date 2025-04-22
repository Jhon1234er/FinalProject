# utils.py
import os
import base64
from email.mime.text import MIMEText
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse

# Solo necesitamos permiso para enviar correos
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

def obtener_servicio_gmail():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credenciales_google/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    service = build('gmail', 'v1', credentials=creds)
    return service
def enviar_correo_recuperacion(request, usuario):
    service = obtener_servicio_gmail()

    # Generar UID y token seguros
    uid = urlsafe_base64_encode(force_bytes(usuario.pk))
    token = default_token_generator.make_token(usuario)

    # Construir la URL segura
    enlace = request.build_absolute_uri(
        reverse('reset_password', kwargs={'uidb64': uid, 'token': token})
    )

    cuerpo = f"""
    Hola {usuario.username},
    
    Has solicitado restablecer tu contraseña. Haz clic en el siguiente enlace:

    {enlace}

    Si no fuiste tú, puedes ignorar este mensaje.
    """

    mensaje = MIMEText(cuerpo)
    mensaje['to'] = usuario.email
    mensaje['from'] = 'tucorreo@gmail.com'
    mensaje['subject'] = 'Recuperación de contraseña'

    raw = base64.urlsafe_b64encode(mensaje.as_bytes()).decode()
    service.users().messages().send(userId="me", body={'raw': raw}).execute()