"""
URL configuration for DjIzel project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from Izelapp.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Home
    path('admin/', admin.site.urls),
    path('', home, name='home'),

    # region Medicos
    path('medico/registrar/', crear_medico, name='registrar_medico'),
    path('medico/listar/', lista_medico, name='listar_medico'),
    path('medico/actualizar/<int:id>/', actualizar_medico, name='actualizar_medico'),
    path('medico/eliminar/<int:id>/', eliminar_medico, name='eliminar_medico'),
    # endregion
    # region HorarioMedico 
    path('horario/registrar/', crear_horario_medico, name='registrar_horario_medico'),
    path('horario/listar/', lista_horario_medico, name='listar_horario_medico'),
    path('horario/actualizar/<int:id>/', actualizar_horario_medico, name='actualizar_horario_medico'),
    path('horario/eliminar/<int:id>/', eliminar_horario_medico, name='eliminar_horario_medico'),
    # endregion

    # region IT 
    path('ti/registrar/', crear_it, name='registrar_it'),
    path('ti/listar/', lista_it, name='listar_it'),
    path('ti/actualizar/<int:id>/', actualizar_it, name='actualizar_it'),
    path('ti/eliminar/<int:id>/', eliminar_it, name='eliminar_it'),
    # endregion

    # region Administrador 
    path('administrador/registrar/', crear_administrador, name='registrar_administrador'),
    path('administrador/listar/', lista_administrador, name='listar_administrador'),
    path('administrador/actualizar/<int:id>/', actualizar_administrador, name='actualizar_administrador'),
    path('administrador/eliminar/<int:id>/', eliminar_administrador, name='eliminar_administrador'),
    # endregion

    # region Empleado 
    path('empleado/registrar/', crear_empleado, name='registrar_empleado'),
    path('empleado/listar/', lista_empleado, name='listar_empleado'),
    path('empleado/actualizar/<int:id>/', actualizar_empleado, name='actualizar_empleado'),
    path('empleado/eliminar/<int:id>/', eliminar_empleado, name='eliminar_empleado'),
    # endregion

    # region Usuario (Usuario Base) 
    path('usuario/insertar/', registrar_usuario, name='registrar_usuario'),
    path('usuario/eliminar/<int:id>/', eliminar_usuario, name='eliminar_usuario'),
    path('usuario/lista/', lista_usuario, name='listar_usuarios'),
    path('usuario/actualizar/<int:id>/', actualizar_usuario, name='actualizar_usuario'),
    path('usuario/detallar/', detallar_usuario, name='detallar_usuario'),
    path('usuario/ver-perfil/', ver_perfil_usuario, name='perfil_usuario'),
    path('usuario/login/', login_usuario, name='login'),
    path('usuario/logout/', logout_usuario, name='logout'),
    # endregion

    # region Paciente 
    path('paciente/registrar/', crear_paciente, name='registrar_paciente'),
    path('paciente/listar/', lista_paciente, name='listar_paciente'),
    path('paciente/actualizar/<int:id>/', actualizar_paciente, name='actualizar_paciente'),
    path('paciente/eliminar/<int:id>/', eliminar_paciente, name='eliminar_paciente'),
    # endregion

    # region Consulta 
    path('consulta/registrar/', crear_consulta, name='registrar_consulta'),
    path('consulta/listar/', lista_consulta, name='listar_consulta'),
    path('consulta/actualizar/<int:id>/', actualizar_consulta, name='actualizar_consulta'),
    path('consulta/eliminar/<int:id>/', eliminar_consulta, name='eliminar_consulta'),
    # endregion

    # region PerfilPaciente 
    path('perfil/registrar/', crear_perfil_paciente, name='registrar_perfil_paciente'),
    path('perfil/listar/', lista_perfil_paciente, name='listar_perfil_paciente'),
    # endregion

    # region Antecedente 
    path('antecedente/registrar/', crear_antecedente, name='registrar_antecedente'),
    path('antecedente/listar/', lista_antecedente, name='listar_antecedente'),
    # endregion

    # region Vacuna 
    path('vacuna/registrar/', crear_vacuna, name='registrar_vacuna'),
    path('vacuna/listar/', lista_vacuna, name='listar_vacuna'),
    path('vacuna/eliminar/<int:id>/', eliminar_vacuna, name='eliminar_vacuna'),
    # endregion

    # region DatoQuirurgico 
    path('quirurgico/registrar/', crear_dato_quirurgico, name='registrar_dato_quirurgico'),
    path('quirurgico/listar/', lista_dato_quirurgico, name='listar_dato_quirurgico'),
    # endregion

    # region HistoriaClinica 
    path('historia/registrar/', crear_historia_clinica, name='registrar_historia_clinica'),
    path('historia/listar/', lista_historia_clinica, name='listar_historia_clinica'),
    # endregion

    # region DatoAntropometrico 
    path('antropometrico/registrar/', crear_dato_antropometrico, name='registrar_dato_antropometrico'),
    path('antropometrico/listar/', lista_dato_antropometrico, name='listar_dato_antropometrico'),
    # endregion

    # region Cita 
    path('cita/registrar/', crear_cita, name='registrar_cita'),
    path('cita/listar/', lista_cita, name='listar_cita'),
    # endregion

    # region CertificadoIncapacidad 
    path('certificado/registrar/', crear_certificado_incapacidad, name='registrar_certificado_incapacidad'),
    path('certificado/listar/', lista_certificado_incapacidad, name='listar_certificado_incapacidad'),
    # endregion

    # region RecetaMedica 
    path('receta/registrar/', crear_receta_medica, name='registrar_receta_medica'),
    path('receta/listar/', lista_receta_medica, name='listar_receta_medica'),
    path('receta/eliminar/<int:id>/', eliminar_receta_medica, name='eliminar_receta_medica'),
    # endregion

    # region OrdenMedica 
    path('orden/registrar/', crear_orden_medica, name='registrar_orden_medica'),
    path('orden/listar/', lista_orden_medica, name='listar_orden_medica'),
    # endregion

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
