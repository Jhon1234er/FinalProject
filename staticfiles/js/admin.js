// static/js/admin.js

document.addEventListener('DOMContentLoaded', function () {
  const botones = document.querySelectorAll('.actions a');
  const contenedor = document.getElementById('contenido-dinamico');
  const bienvenida = document.querySelector('.bienvenida-mensaje');

  botones.forEach(boton => {
    boton.addEventListener('click', async (e) => {
      e.preventDefault();
      const panel = boton.getAttribute('onclick')?.match(/'(.*?)'/)?.[1];
      if (!panel) return;

      let url = '';
      switch (panel) {
        case 'pacientes':
          url = '/paciente/listar/';
          break;
        case 'medicos':
          url = '/medico/listar/';
          break;
        case 'citas':
          url = '/admin/citas/';
          break;
        case 'crear':
          url = '/gestionar_disponibilidad/';
          break;
        default:
          return;
      }

      try {
        const respuesta = await fetch(url, {
          headers: {
            'X-Requested-With': 'XMLHttpRequest'
          }
        });

        if (!respuesta.ok) throw new Error('Error al cargar el contenido');

        const html = await respuesta.text();

        // Ocultar bienvenida solo si no se está repitiendo el botón
        if (bienvenida) bienvenida.style.display = 'none';

        contenedor.innerHTML = html;
        contenedor.scrollIntoView({ behavior: 'smooth' });

      } catch (err) {
        console.error(err);
        contenedor.innerHTML = `<p>Error al cargar el panel: ${err.message}</p>`;
      }
    });
  });
});
