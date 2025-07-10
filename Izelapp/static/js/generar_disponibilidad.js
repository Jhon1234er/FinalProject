document.addEventListener("DOMContentLoaded", function () {
  const seleccionados = new Set();
  const botones = document.querySelectorAll('.medico-btn');
  const inputOculto = document.getElementById('medicos_seleccionados');

  botones.forEach(btn => {
    btn.addEventListener('click', () => {
      const id = btn.dataset.id;
      btn.classList.toggle('activo');
      if (seleccionados.has(id)) {
        seleccionados.delete(id);
      } else {
        seleccionados.add(id);
      }
      inputOculto.value = Array.from(seleccionados).join(',');
    });
  });

  const form = document.getElementById("disponibilidad-form");
  const horaInicioInput = form.querySelector('input[name="hora_inicio"]');
  const horaFinInput = form.querySelector('input[name="hora_fin"]');
  const duracionInput = form.querySelector('select[name="duracion"]');
  const bloquesContenedor = document.getElementById("bloques-horarios");

  function generarBloques() {
    bloquesContenedor.innerHTML = "";
    const horaInicio = horaInicioInput.value;
    const horaFin = horaFinInput.value;
    const duracion = parseInt(duracionInput.value);

    if (!horaInicio || !horaFin || !duracion) return;

    let actual = new Date(`2000-01-01T${convertirHora24(horaInicio)}`);
    const fin = new Date(`2000-01-01T${convertirHora24(horaFin)}`);

    while (actual.getTime() + duracion * 60000 <= fin.getTime()) {
      const siguiente = new Date(actual.getTime() + duracion * 60000);
      const desde24 = actual.toTimeString().slice(0, 5);    // hh:mm para backend
      const hasta24 = siguiente.toTimeString().slice(0, 5);
      const desde12 = formato12h(actual);                  // hh:mm am/pm para mostrar
      const hasta12 = formato12h(siguiente);

      const bloque = document.createElement("label");
      bloque.className = "bloque-horario";
      bloque.innerHTML = `
        <input type="checkbox" name="bloques" value="${desde24}-${hasta24}" checked>
        <span>${desde12} - ${hasta12}</span>
      `;
      bloquesContenedor.appendChild(bloque);
      actual = siguiente;
    }
  }

  function convertirHora24(horaAMPM) {
    const date = new Date(`2000-01-01 ${horaAMPM}`);
    return date.toTimeString().slice(0, 5); // "HH:MM"
  }

  function formato12h(date) {
    return date.toLocaleTimeString('es-CO', {
      hour: '2-digit',
      minute: '2-digit',
      hour12: true
    }).toLowerCase(); // "10:00 am"
  }

  horaInicioInput.addEventListener('change', generarBloques);
  horaFinInput.addEventListener('change', generarBloques);
  duracionInput.addEventListener('change', generarBloques);
});
