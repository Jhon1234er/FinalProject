// Mapeo de permisos JSON
const permisosJson = {
    "ODONTOLOGIA": {
        "medico": {"ver_pacientes": true, "editar_pacientes": true, "ver_historia_clinica": true, "realizar_tratamientos": true},
        "auxiliar": {"ver_pacientes": true, "realizar_tratamientos": false},
        "administrador": {"ver_pacientes": true, "editar_pacientes": true, "ver_historia_clinica": true, "gestion_usuarios": true}
    },
    "CIRUGIA": {
        "medico": {"ver_pacientes": true, "realizar_cirugia": true, "ver_historia_clinica": true},
        "auxiliar": {"ver_pacientes": true, "realizar_cirugia": false},
        "administrador": {"ver_pacientes": true, "realizar_cirugia": true, "ver_historia_clinica": true, "gestion_usuarios": true}
    },
    "GENERAL": {
        "medico": {"ver_pacientes": true, "ver_historia_clinica": true},
        "auxiliar": {"ver_pacientes": true, "ver_historia_clinica": false},
        "administrador": {"ver_pacientes": true, "ver_historia_clinica": true, "gestion_usuarios": true}
    },
    "RAYOS_X": {
        "medico": {"ver_pacientes": true, "ver_imagenes": true, "realizar_imagenes": true},
        "auxiliar": {"ver_pacientes": true, "ver_imagenes": false},
        "administrador": {"ver_pacientes": true, "ver_imagenes": true, "realizar_imagenes": true, "gestion_usuarios": true}
    }
};

// Función para actualizar permisos según la selección
function actualizarPermisos() {
    const centro = document.getElementById('centro_administracion').value;
    const permisos = permisosJson[centro]["administrador"];
    
    // Actualizamos las casillas de verificación según los permisos
    for (let permiso in permisos) {
        const checkbox = document.querySelector(`input[name="${permiso}"]`);
        if (checkbox) {
            checkbox.checked = permisos[permiso];
        }
    }
}

// Llamar la función al cargar la página para actualizar los permisos predeterminados
window.onload = actualizarPermisos;
