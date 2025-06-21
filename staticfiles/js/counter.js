document.addEventListener("DOMContentLoaded", () => {
  const counters = document.querySelectorAll('.contador');
  const options = {
    root: null,
    rootMargin: '0px',
    threshold: 0.6
  };

  const startCounter = (entry) => {
    const el = entry.target;
    const target = +el.getAttribute('data-count');
    let count = 0;
    const increment = target / 50;

    const updateCounter = () => {
      if (count < target) {
        count += increment;
        el.textContent = Math.ceil(count).toLocaleString();
        requestAnimationFrame(updateCounter);
      } else {
        el.textContent = target.toLocaleString();
      }
    };

    updateCounter();
  };

  const observer = new IntersectionObserver((entries, obs) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        startCounter(entry);
        obs.unobserve(entry.target);
      }
    });
  }, options);

  counters.forEach(counter => observer.observe(counter));
});
