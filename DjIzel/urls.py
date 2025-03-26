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
    #region Home
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    #endregion


    #region Inicio Sesion 
    path('login/', login_usuario, name='login'), 
    path('logout/', logout_usuario, name='logout'),
    path('detallar_usuario/', detallar_usuario, name='detallar_usuario'),






    # region Usuario 
    path('usuario/insertar/', registrar_usuario, name='registrar_usuario'),
    path('usuario/eliminar/<int:id>/', eliminar_usuario, name='eliminar_usuario'),
    path('usuario/lista/', lista_usuario, name='listar_usuarios'),
    path('usuario/actualizar/<int:id>/', actualizar_usuario, name='actualizar_usuario'),
    path('usuario/eliminar_imagen/', eliminar_imagen_usuario, name='eliminar_imagen_usuario'),
    # endregion





    # region Medicos
    path('medico/registrar/', registrar_medico, name='registrar_medico'),
    path('medico/listar/', lista_medico, name='listar_medico'),
    path('medico/actualizar/<int:id>/', actualizar_medico, name='actualizar_medico'),
    path('medico/eliminar/<int:id>/', eliminar_medico, name='eliminar_medico'),
    path('perfil/', login_usuario, name='perfil'),
    # endregion




    # region IT 
    path('ti/registrar/', registrar_ti, name='registrar_ti'),
    path('ti/listar/', lista_ti, name='listar_ti'),
    path('ti/actualizar/<int:id>/', actualizar_ti, name='actualizar_ti'),
    path('ti/eliminar/<int:id>/', eliminar_ti, name='eliminar_ti'),
    # endregion





    # region Administrador 
    path('administrador/registrar/', registrar_administrador, name='registrar_administrador'),
    path('administrador/listar/', lista_administrador, name='listar_administrador'),
    path('administrador/actualizar/<int:id>/', actualizar_administrador, name='actualizar_administrador'),
    path('administrador/eliminar/<int:id>/', eliminar_administrador, name='eliminar_administrador'),
    # endregion



    # region Paciente 
    path('paciente/registrar/', registrar_paciente, name='registrar_paciente'),
    path('paciente/listar/', lista_paciente, name='listar_paciente'),
    path('paciente/actualizar/<int:id>/', actualizar_paciente, name='actualizar_paciente'),
    path('paciente/eliminar/<int:id>/', eliminar_paciente, name='eliminar_paciente'),
    # endregion




    #region Auxiliar
    path('auxiliar/registrar/', registrar_auxiliar, name='registrar_auxiliar'),
    path('auxiliar/lista/', lista_auxiliar, name='listar_auxiliares'),
    path('auxiliar/actualizar/<int:id>/', actualizar_auxiliar, name='actualizar_auxiliar'),
    path('auxiliar/eliminar/<int:id>/', eliminar_auxiliar, name='eliminar_auxiliar'),
    #endregion






    # region HorarioMedico 
    path('horario/registrar/', registrar_horario_medico, name='registrar_horario_medico'),
    path('horario/listar/', lista_horario_medico, name='listar_horario_medico'),
    path('horario/actualizar/<int:id>/', actualizar_horario_medico, name='actualizar_horario_medico'),
    path('horario/eliminar/<int:id>/', eliminar_horario_medico, name='eliminar_horario_medico'),
    # endregion





    # region Consulta 
    path('consulta/registrar/', registrar_consulta, name='registrar_consulta'),
    path('consulta/listar/', lista_consulta, name='listar_consulta'),
    path('consulta/actualizar/<int:id>/', actualizar_consulta, name='actualizar_consulta'),
    path('consulta/eliminar/<int:id>/', eliminar_consulta, name='eliminar_consulta'),
    # endregion





    # region PerfilPaciente 
    path('perfil/registrar/', registrar_perfil_paciente, name='registrar_perfil_paciente'),
    path('perfil/listar/', lista_perfil_paciente, name='listar_perfil_paciente'),
    # endregion






    # region Antecedente 
    path('antecedente/registrar/', crear_antecedente, name='registrar_antecedente'),
    path('antecedente/listar/', lista_antecedente, name='listar_antecedente'),
    # endregion






    # region Vacuna 
    path('vacuna/registrar/', registrar_vacuna, name='registrar_vacuna'),
    path('vacuna/listar/', lista_vacuna, name='listar_vacuna'),
    path('vacuna/eliminar/<int:id>/', eliminar_vacuna, name='eliminar_vacuna'),
    # endregion






    # region DatoQuirurgico 
    path('quirurgico/registrar/', registrar_dato_quirurgico, name='registrar_dato_quirurgico'),
    path('quirurgico/listar/', lista_dato_quirurgico, name='listar_dato_quirurgico'),
    # endregion






    # region HistoriaClinica 
    path('historia/registrar/', registrar_historia_clinica, name='registrar_historia_clinica'),
    path('historia/listar/', lista_historia_clinica, name='listar_historia_clinica'),
    # endregion






    # region DatoAntropometrico 
    path('antropometrico/registrar/', registrar_dato_antropometrico, name='registrar_dato_antropometrico'),
    path('antropometrico/listar/', lista_dato_antropometrico, name='listar_dato_antropometrico'),
    # endregion






    # region Cita 
    path('cita/registrar/', registrar_cita, name='registrar_cita'),
    path('cita/listar/', lista_cita, name='listar_cita'),
    # endregion






    # region CertificadoIncapacidad 
    path('certificado/registrar/', registrar_certificado_incapacidad, name='registrar_certificado_incapacidad'),
    path('certificado/listar/', lista_certificado_incapacidad, name='listar_certificado_incapacidad'),
    # endregion






    # region RecetaMedica 
    path('receta/registrar/', registrar_receta_medica, name='registrar_receta_medica'),
    path('receta/listar/', lista_receta_medica, name='listar_receta_medica'),
    path('receta/eliminar/<int:id>/', eliminar_receta_medica, name='eliminar_receta_medica'),
    # endregion






    # region OrdenMedica 
    path('orden/registrar/', registrar_orden_medica, name='registrar_orden_medica'),
    path('orden/listar/', lista_orden_medica, name='listar_orden_medica'),
    # endregion




    #region Disponibilidad

    path('calendario/', calendario, name='calendario'),
    path('obtener_disponibilidad/', obtener_disponibilidad, name='obtener_disponibilidad'),
    path('verificar_disponibilidad/', verificar_disponibilidad, name='verificar_disponibilidad'),
    path('confirmar_cita/', confirmar_cita, name='confirmar_cita'),
    path('gestionar_disponibilidad/', gestionar_disponibilidad, name='gestionar_disponibilidad'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
