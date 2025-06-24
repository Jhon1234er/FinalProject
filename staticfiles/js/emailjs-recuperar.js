document.addEventListener("DOMContentLoaded", function () {
  emailjs.init("nGBBTWGl1H3n6cggD");  // Ej: "nGBBTWGl1H3n6cggD"

  const form = document.getElementById("recuperar-form");
  const mensaje = document.getElementById("mensaje");

  form.addEventListener("submit", async function (e) {
    e.preventDefault();

    const tipo_doc = document.getElementById("tipo_doc").value;
    const num_doc = document.getElementById("num_doc").value;

    if (!tipo_doc || !num_doc) {
      mensaje.textContent = "Todos los campos son obligatorios.";
      mensaje.style.color = "red";
      return;
    }

    try {
      const response = await fetch("/api/buscar-usuario/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": getCSRFToken(),
        },
        body: JSON.stringify({ tipo_doc, num_doc }),
      });

      if (!response.ok) throw new Error("Usuario no encontrado");

      const data = await response.json();
      const enlace = `http://localhost:8000/restablecer/${data.id}/`;

      console.log("Enviando correo a:", data.email);
      console.log("Enlace de recuperación:", enlace);

      await emailjs.send("service_fk7d6uk", "template_jtgdbau", {
        email: data.email,
        link: enlace,
      });

      mensaje.textContent = `✔ Instrucciones enviadas al correo: ${data.email}`;
      mensaje.style.color = "green";
      form.reset();
    } catch (error) {
      console.error("❌ Error al enviar el correo:", error);
      mensaje.textContent = "❌ No se pudo enviar el correo. Verifica tus datos.";
      mensaje.style.color = "red";
    }
  });

  function getCSRFToken() {
    const name = "csrftoken=";
    const cookies = document.cookie.split(";");
    for (let cookie of cookies) {
      if (cookie.trim().startsWith(name)) {
        return cookie.trim().substring(name.length);
      }
    }
    return "";
  }
});
