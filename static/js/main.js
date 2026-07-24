/**
 * Personal Health & Environmental Wellness Recommendation System
 * Core Client-side Script
 */

document.addEventListener('DOMContentLoaded', () => {
  setupSidebar();
  highlightActiveLink();
});

/**
 * Setup responsiveness controls for the sidebar on mobile views
 */
function setupSidebar() {
  const sidebar = document.querySelector('.sidebar');
  const menuToggle = document.getElementById('menu-toggle');
  
  if (!sidebar || !menuToggle) return;

  // Create overlay element dynamically if not present
  let overlay = document.querySelector('.sidebar-overlay');
  if (!overlay) {
    overlay = document.createElement('div');
    overlay.className = 'sidebar-overlay';
    document.body.appendChild(overlay);
  }

  // Toggle mobile sidebar
  menuToggle.addEventListener('click', () => {
    sidebar.classList.toggle('mobile-open');
    overlay.classList.toggle('active');
  });

  // Close when clicking outside (overlay)
  overlay.addEventListener('click', () => {
    sidebar.classList.remove('mobile-open');
    overlay.classList.remove('active');
  });

  // Close mobile sidebar on window resize to desktop width
  window.addEventListener('resize', () => {
    if (window.innerWidth > 992) {
      sidebar.classList.remove('mobile-open');
      overlay.classList.remove('active');
    }
  });
}

/**
 * Set active status on sidebar links based on the current URL path
 */
function highlightActiveLink() {
  const currentPath = window.location.pathname;
  const sidebarLinks = document.querySelectorAll('.sidebar-link');

  sidebarLinks.forEach(link => {
    const href = link.getAttribute('href');
    if (href && (currentPath === href || (href !== '/' && currentPath.startsWith(href)))) {
      link.classList.add('active');
    } else {
      link.classList.remove('active');
    }
  });
}
