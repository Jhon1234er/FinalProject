document.addEventListener("DOMContentLoaded", () => {
  const toggleBtn = document.getElementById("toggle-citas");
  const agendadas = document.getElementById("citas-agendadas");
  const canceladas = document.getElementById("citas-canceladas");

  if (toggleBtn && agendadas && canceladas) {
    toggleBtn.addEventListener("click", () => {
      const mostrandoAgendadas = agendadas.style.display !== "none";
      agendadas.style.display = mostrandoAgendadas ? "none" : "grid";
      canceladas.style.display = mostrandoAgendadas ? "grid" : "none";
      toggleBtn.textContent = mostrandoAgendadas ? "Ver Citas Agendadas" : "Ver Citas Perdidas";
    });
  }

  const flashMessage = document.getElementById("flash-message");
  if (flashMessage) {
    setTimeout(() => flashMessage.style.display = "none", 2000);
  }

  const cancelarBtns = document.querySelectorAll(".cancelar-btn");
  cancelarBtns.forEach(btn => {
    btn.addEventListener("click", function (e) {
      e.preventDefault();
      const url = btn.getAttribute("href");

      Swal.fire({
        title: "¿Cancelar esta cita?",
        text: "Una vez cancelada, no podrás recuperarla.",
        icon: "warning",
        showCancelButton: true,
        confirmButtonColor: "#d33",
        cancelButtonColor: "#3085d6",
        confirmButtonText: "Sí, cancelar",
        cancelButtonText: "No"
      }).then((result) => {
        if (result.isConfirmed) {
          window.location.href = url;
        }
      });
    });
  });
});
