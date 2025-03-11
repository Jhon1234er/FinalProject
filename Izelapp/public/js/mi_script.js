document.addEventListener("DOMContentLoaded", function() {
    const tipoEmpleadoSelect = document.getElementById("tipo_empleado");
    const formularioEmpleadoDiv = document.getElementById("formulario_tipo_empleado");
    const formularioEmpleado = document.getElementById("empleado_form");
    const formularioAdministrador = document.getElementById("administrador_form");
    const formularioIt = document.getElementById("it_form");
    const formularioMedico = document.getElementById("medico_form");

    tipoEmpleadoSelect.addEventListener("change", function() {
        // Ocultar todos los formularios
        formularioEmpleado.style.display = "none";
        formularioAdministrador.style.display = "none";
        formularioIt.style.display = "none";
        formularioMedico.style.display = "none";

        // Mostrar el formulario correspondiente según la selección
        const tipoEmpleado = this.value;
        if (tipoEmpleado === "empleado") {
            formularioEmpleado.style.display = "block";
        } else if (tipoEmpleado === "administrador") {
            formularioAdministrador.style.display = "block";
        } else if (tipoEmpleado === "it") {
            formularioIt.style.display = "block";
        } else if (tipoEmpleado === "medico") {
            formularioMedico.style.display = "block";
        }
    });
});
