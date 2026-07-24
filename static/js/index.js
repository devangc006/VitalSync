/**
 * Landing Page Animations and Interaction
 */

document.addEventListener('DOMContentLoaded', () => {
  setupScrollAnimations();
});

/**
 * Uses IntersectionObserver to trigger entry animations on feature cards and sections
 */
function setupScrollAnimations() {
  const animatedElements = document.querySelectorAll('.feature-card, .step-card, .about-section, .cta-section');
  
  const observerOptions = {
    root: null,
    rootMargin: '0px',
    threshold: 0.15
  };

  const observer = new IntersectionObserver((entries, observer) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        // Stop observing once animated in
        observer.unobserve(entry.target);
      }
    });
  }, observerOptions);

  animatedElements.forEach((el, index) => {
    // Add preparation class
    el.classList.add('fade-in-element');
    // Stagger animation timing a bit for children
    if (el.classList.contains('feature-card') || el.classList.contains('step-card')) {
      el.style.transitionDelay = `${index * 0.1}s`;
    }
    observer.observe(el);
  });
}

// Append fade-in styles dynamically if needed
const style = document.createElement('style');
style.textContent = `
  .fade-in-element {
    opacity: 0;
    transform: translateY(30px);
    transition: opacity 0.8s cubic-bezier(0.16, 1, 0.3, 1), transform 0.8s cubic-bezier(0.16, 1, 0.3, 1);
  }
  .fade-in-element.visible {
    opacity: 1;
    transform: translateY(0);
  }
`;
document.head.appendChild(style);
