window.addEventListener("scroll", function () {
  const texto = document.getElementById("deslizar-texto");
  if (window.scrollY > 100) {
    texto.style.opacity = "0";
  } else {
    texto.style.opacity = "1";
  }
});

// Efecto Kokonut Attract Button
const attractButtons = document.querySelectorAll(".btn-attract");

attractButtons.forEach((button) => {
  const particles = [];
  const particleCount = 12;
  const radius = 50;

  // Crear partículas
  for (let i = 0; i < particleCount; i++) {
    const particle = document.createElement("div");
    particle.classList.add("attract-particle");
    const angle = (Math.PI * 2 * i) / particleCount;
    const x = Math.cos(angle) * radius;
    const y = Math.sin(angle) * radius;
    particle.style.transform = `translate(${x}px, ${y}px)`;
    button.appendChild(particle);
    particles.push(particle);
  }

  button.addEventListener("mouseenter", () => {
    particles.forEach((p) => {
      p.style.transform = `translate(0px, 0px)`;
      p.style.opacity = "1";
    });
  });

  button.addEventListener("mouseleave", () => {
    particles.forEach((p, i) => {
      const angle = (Math.PI * 2 * i) / particleCount;
      const x = Math.cos(angle) * radius;
      const y = Math.sin(angle) * radius;
      p.style.transform = `translate(${x}px, ${y}px)`;
      p.style.opacity = "0.4";
    });
  });
});