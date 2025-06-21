document.addEventListener("DOMContentLoaded", function () {
  const ctx = document.getElementById('citasChart').getContext('2d');

  const data = {
    labels: ['Asistidas', 'Perdidas','No Pagadas'],
    datasets: [{
      data: [75, 25, 10], // Puedes cambiar estos valores dinámicamente
      backgroundColor: ['#4CAF50', '#F44336', '#f1c40f'],
      hoverOffset: 10
    }]
  };

  const config = {
    type: 'doughnut',
    data: data,
    options: {
      responsive: true,
      plugins: {
        legend: {
          position: 'bottom',
          onClick: (e, legendItem, legend) => {
            const label = legendItem.text;
            alert(`Has hecho clic en: ${label}`);
          }
        },
        tooltip: {
          callbacks: {
            label: function(context) {
              const value = context.raw;
              return `${context.label}: ${value}%`;
            }
          }
        }
      }
    }
  };

  new Chart(ctx, config);
});
