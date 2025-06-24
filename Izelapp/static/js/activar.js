document.addEventListener("DOMContentLoaded", function () {
  // ✅ Activar Select2
  $('.select2').select2({
    width: '100%',
    placeholder: 'Selecciona una opción',
    allowClear: true
  });

  // ✅ Flatpickr para fechas futuras (ej. disponibilidad médica)
  if (typeof flatpickr !== 'undefined') {
    flatpickr(".datepicker", {
      dateFormat: "Y-m-d",
      locale: "es",
      minDate: "today",
      altInput: true,
      altFormat: "d/m/Y"
    });
  } else {
    console.warn("Flatpickr no está disponible. Verifica la carga del script.");
  }

  // ✅ Activar intlTelInput para campos de teléfono
  const telefonoInput =
    document.querySelector("#telefono-input") ||
    document.querySelector("#id_telefono");

  if (telefonoInput && typeof window.intlTelInput === "function") {
    const iti = window.intlTelInput(telefonoInput, {
      initialCountry: "co",
      separateDialCode: true,
      preferredCountries: ["co", "mx", "es", "us", "ar"],
      nationalMode: false,
      utilsScript: "https://cdn.jsdelivr.net/npm/intl-tel-input@18.1.1/build/js/utils.js"
    });

    const form = telefonoInput.closest("form");
    if (form) {
      form.addEventListener("submit", function () {
        if (iti.isValidNumber()) {
          telefonoInput.value = iti.getNumber(); // ej. +573001234567
        }
      });
    }
  } else {
    console.warn("Campo de teléfono no encontrado o intlTelInput no disponible.");
  }

  // ✅ Bloques horarios (solo si existe el formulario de disponibilidad)
  const form = document.getElementById("disponibilidad-form");
  if (form) {
    const horaInicioInput = form.querySelector('input[name="hora_inicio"]');
    const horaFinInput = form.querySelector('input[name="hora_fin"]');
    const duracionInput = form.querySelector('select[name="duracion"]');
    const bloquesContenedor = document.getElementById("bloques-horarios");

    function generarBloques() {
      bloquesContenedor.innerHTML = "";

      const horaInicio = horaInicioInput.value;
      const horaFin = horaFinInput.value;
      const duracion = parseInt(duracionInput.value);

      if (horaInicio && horaFin && duracion) {
        let actual = new Date(`1970-01-01T${horaInicio}`);
        const fin = new Date(`1970-01-01T${horaFin}`);

        while (actual.getTime() + duracion * 60000 <= fin.getTime()) {
          const siguiente = new Date(actual.getTime() + duracion * 60000);
          const desde = actual.toTimeString().slice(0, 5);
          const hasta = siguiente.toTimeString().slice(0, 5);

          const bloque = document.createElement("label");
          bloque.innerHTML = `
            <input type="checkbox" name="bloques" value="${desde}-${hasta}" checked>
            ${desde} - ${hasta}
          `;
          bloquesContenedor.appendChild(bloque);
          actual = siguiente;
        }
      }
    }

    horaInicioInput.addEventListener('change', generarBloques);
    horaFinInput.addEventListener('change', generarBloques);
    duracionInput.addEventListener('change', generarBloques);
  }
});