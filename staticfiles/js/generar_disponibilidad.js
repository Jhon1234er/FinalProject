// generar_disponibilidad.js

document.addEventListener("DOMContentLoaded", function () {
  const seleccionados = new Set();
  const botones = document.querySelectorAll('.medico-btn');
  const inputOculto = document.getElementById('medicos_seleccionados');

  botones.forEach(btn => {
    btn.addEventListener('click', () => {
      const id = btn.dataset.id;
      if (seleccionados.has(id)) {
        seleccionados.delete(id);
        btn.classList.remove('activo');
      } else {
        seleccionados.add(id);
        btn.classList.add('activo');
      }
      inputOculto.value = Array.from(seleccionados).join(',');
    });
  });

  // Bloques horarios automáticos
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

    console.log("Hora inicio:", horaInicio);
    console.log("Hora fin:", horaFin);
    console.log("Duración:", duracion);

    if (!horaInicio || !horaFin || !duracion) return;

    let actual = new Date(`2000-01-01T${horaInicio}`);
    const fin = new Date(`2000-01-01T${horaFin}`);

    while (actual.getTime() + duracion * 60000 <= fin.getTime()) {
      const siguiente = new Date(actual.getTime() + duracion * 60000);
      const desde = actual.toTimeString().slice(0, 5);
      const hasta = siguiente.toTimeString().slice(0, 5);

      const bloque = document.createElement("label");
      bloque.className = "bloque-horario";
      bloque.innerHTML = `
        <input type="checkbox" name="bloques" value="${desde}-${hasta}" checked>
        <span>${desde} - ${hasta}</span>
      `;
      bloquesContenedor.appendChild(bloque);
      actual = siguiente;
    }
  }

  horaInicioInput.addEventListener('change', generarBloques);
  horaFinInput.addEventListener('change', generarBloques);
  duracionInput.addEventListener('change', generarBloques);
});