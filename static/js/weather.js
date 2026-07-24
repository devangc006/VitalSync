/**
 * Dynamic Weather Background and Animation Effects
 */

document.addEventListener('DOMContentLoaded', () => {
  renderAtmosphericEffects();
});

/**
 * Creates dynamic particles (e.g. rain droplets) for the matching weather type
 */
function renderAtmosphericEffects() {
  const wrapper = document.querySelector('.weather-page-wrapper');
  if (!wrapper) return;

  const isRain = wrapper.classList.contains('condition-rain') || 
                 wrapper.classList.contains('condition-drizzle') || 
                 wrapper.classList.contains('condition-thunderstorm');

  if (isRain) {
    createRainParticles(wrapper);
  }
}

function createRainParticles(container) {
  const dropCount = 40;
  const animContainer = container.querySelector('.rain-drops') || container;
  
  for (let i = 0; i < dropCount; i++) {
    const drop = document.createElement('div');
    drop.className = 'rain-drop-particle';
    drop.style.left = `${Math.random() * 100}%`;
    drop.style.animationDelay = `${Math.random() * 2}s`;
    drop.style.animationDuration = `${0.5 + Math.random() * 0.5}s`;
    animContainer.appendChild(drop);
  }
  
  // Inject rain droplet styling dynamically
  const style = document.createElement('style');
  style.textContent = `
    .rain-drop-particle {
      position: absolute;
      top: -10px;
      width: 1px;
      height: 15px;
      background: linear-gradient(transparent, rgba(59, 130, 246, 0.4));
      animation: drop-fall linear infinite;
      z-index: 1;
    }
    @keyframes drop-fall {
      to {
        transform: translateY(300px);
      }
    }
  `;
  document.head.appendChild(style);
}
