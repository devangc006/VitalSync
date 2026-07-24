/**
 * Dashboard Client Actions & Chart Renderings
 */

document.addEventListener('DOMContentLoaded', () => {
  displayTodayDate();
  setupHydrationTracker();
  renderWeeklyChart();
});

/**
 * Format and insert today's calendar date in the dashboard
 */
function displayTodayDate() {
  const dateEl = document.getElementById('current-date');
  if (!dateEl) return;
  
  const options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
  const today = new Date();
  dateEl.textContent = today.toLocaleDateString('en-US', options);
}

/**
 * Handles adding water consumption in increments of 250ml
 */
function setupHydrationTracker() {
  const logBtn = document.getElementById('log-water-btn');
  const loggedText = document.getElementById('logged-water');
  const progressBar = document.getElementById('water-progress-bar');

  if (!logBtn || !loggedText || !progressBar) return;

  let currentWater = 0.0;
  
  logBtn.addEventListener('click', () => {
    // Increment by 250ml (0.25L)
    currentWater = Math.min(currentWater + 0.25, dailyWaterGoal);
    
    // Update texts
    loggedText.textContent = currentWater.toFixed(2);
    
    // Update progress bar percentage width
    const percentage = (currentWater / dailyWaterGoal) * 100;
    progressBar.style.width = `${percentage}%`;

    // Visual effect on success
    if (currentWater >= dailyWaterGoal) {
      logBtn.disabled = true;
      logBtn.innerHTML = '<i class="fas fa-check"></i> Goal Met!';
      logBtn.style.borderColor = 'var(--accent-mint)';
      logBtn.style.color = 'var(--accent-mint)';
      logBtn.style.background = 'rgba(16, 185, 129, 0.1)';
    }
  });
}

/**
 * Render standard line/bar chart using Chart.js
 */
function renderWeeklyChart() {
  const ctx = document.getElementById('health-chart');
  if (!ctx) return;

  const chartColors = {
    water: '#3b82f6',
    activity: '#06b6d4',
    grid: 'rgba(255, 255, 255, 0.05)',
    text: '#9ca3af'
  };

  new Chart(ctx, {
    type: 'line',
    data: {
      labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
      datasets: [
        {
          label: 'Water Intake (Liters)',
          data: [2.1, 2.4, 2.0, 2.8, 2.5, 1.8, 2.2],
          borderColor: chartColors.water,
          backgroundColor: 'rgba(59, 130, 246, 0.1)',
          borderWidth: 2,
          fill: true,
          tension: 0.3
        },
        {
          label: 'Activity Duration (Mins)',
          data: [30, 45, 20, 60, 40, 90, 50],
          borderColor: chartColors.activity,
          backgroundColor: 'rgba(6, 182, 212, 0.1)',
          borderWidth: 2,
          fill: true,
          tension: 0.3,
          yAxisID: 'y1'
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        x: {
          grid: { color: chartColors.grid },
          ticks: { color: chartColors.text, font: { family: 'Outfit' } }
        },
        y: {
          type: 'linear',
          display: true,
          position: 'left',
          grid: { color: chartColors.grid },
          ticks: { color: chartColors.text, font: { family: 'Outfit' } },
          title: { display: true, text: 'Liters', color: chartColors.text }
        },
        y1: {
          type: 'linear',
          display: true,
          position: 'right',
          grid: { drawOnChartArea: false }, // Avoid duplicate lines
          ticks: { color: chartColors.text, font: { family: 'Outfit' } },
          title: { display: true, text: 'Minutes', color: chartColors.text }
        }
      },
      plugins: {
        legend: {
          labels: { color: chartColors.text, font: { family: 'Outfit', size: 12 } }
        }
      }
    }
  });
}
