def tipo_usuario_context(request):
    tipo = None
    if request.user.is_authenticated:
        try:
            if hasattr(request.user, 'paciente') and request.user.paciente:
                tipo = 'paciente'
            elif hasattr(request.user, 'administrador') and request.user.administrador:
                tipo = 'administrador'
            elif hasattr(request.user, 'medico') and request.user.medico:
                tipo = 'medico'
        except:
            tipo = None
    return {'tipo_usuario': tipo}
