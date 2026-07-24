/**
 * Recommendations Category Filter Handler
 */

document.addEventListener('DOMContentLoaded', () => {
  setupCategoryFiltering();
});

/**
 * Attaches filter listeners to tabs to dynamically hide/show cards
 */
function setupCategoryFiltering() {
  const tabs = document.querySelectorAll('.filter-tab');
  const cards = document.querySelectorAll('.rec-card');

  if (tabs.length === 0 || cards.length === 0) return;

  tabs.forEach(tab => {
    tab.addEventListener('click', () => {
      // Toggle active states
      tabs.forEach(t => t.classList.remove('active'));
      tab.classList.add('active');

      const filterVal = tab.getAttribute('data-filter');

      cards.forEach(card => {
        const category = card.getAttribute('data-category');
        
        if (filterVal === 'all' || category === filterVal) {
          card.style.display = 'flex';
          // Force fade-in animation
          card.style.opacity = '0';
          setTimeout(() => {
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
          }, 50);
        } else {
          card.style.display = 'none';
        }
      });
    });
  });
}
