document.addEventListener("DOMContentLoaded", function () {
  emailjs.init("TU_USER_ID"); // 🔁 Reemplaza con tu USER ID de EmailJS

  const form = document.getElementById("recuperar-form");
  const mensaje = document.getElementById("mensaje");

  form.addEventListener("submit", function (e) {
    e.preventDefault();

    emailjs.sendForm('TU_SERVICE_ID', 'TU_TEMPLATE_ID', form)
      .then(function () {
        mensaje.textContent = "📬 Correo enviado con éxito.";
        mensaje.style.color = "green";
      }, function (error) {
        mensaje.textContent = "❌ Error al enviar el correo. Intenta más tarde.";
        mensaje.style.color = "red";
      });
  });
});
