window.addEventListener("scroll", function () {
  const texto = document.getElementById("deslizar-texto");
  if (texto) {
    texto.style.opacity = window.scrollY > 100 ? "0" : "1";
  }
});

// Kokonut-style botón con partículas mejoradas
document.addEventListener("DOMContentLoaded", function () {
  const attractButtons = document.querySelectorAll(".btn-attract");

  attractButtons.forEach((button) => {
    const particles = [];
    const particleCount = 14;

    for (let i = 0; i < particleCount; i++) {
      const particle = document.createElement("div");
      particle.classList.add("attract-particle");

      // Posición central
      particle.style.top = "50%";
      particle.style.left = "50%";
      particle.style.position = "absolute";

      // Dispersión irregular
      const angle = Math.random() * 2 * Math.PI;
      const radius = 20 + Math.random() * 30;
      const x = Math.cos(angle) * radius;
      const y = Math.sin(angle) * radius;

      particle.style.transform = `translate(${x}px, ${y}px)`;
      particle.style.opacity = "0.3";

      button.appendChild(particle);
      particles.push({ el: particle, x, y });
    }

    // Hover: retrae al centro
    button.addEventListener("mouseenter", () => {
      particles.forEach((p) => {
        p.el.style.transform = "translate(0, 0)";
        p.el.style.opacity = "1";
      });
    });

    // Mouse out: dispersa de nuevo
    button.addEventListener("mouseleave", () => {
      particles.forEach((p) => {
        p.el.style.transform = `translate(${p.x}px, ${p.y}px)`;
        p.el.style.opacity = "0.3";
      });
    });
  });
});
