/**
 * User Settings Actions & Toggles
 */

document.addEventListener('DOMContentLoaded', () => {
  setupDarkModeTheme();
  setupPasswordMatchValidation();
});

/**
 * Handle switching dark mode style overrides
 */
function setupDarkModeTheme() {
  const toggle = document.getElementById('dark-mode-toggle');
  if (!toggle) return;

  toggle.addEventListener('change', () => {
    if (toggle.checked) {
      document.body.style.filter = 'brightness(0.95) contrast(1.05)';
    } else {
      document.body.style.filter = 'none';
    }
  });
}

/**
 * Validate that new password matches confirm field on client side
 */
function setupPasswordMatchValidation() {
  const form = document.getElementById('password-change-form');
  if (!form) return;

  form.addEventListener('submit', (e) => {
    const newPwd = document.getElementById('new_password').value;
    const confPwd = document.getElementById('confirm_new_password').value;

    if (newPwd.length < 8) {
      e.preventDefault();
      alert('New password must be at least 8 characters long.');
      return;
    }

    if (newPwd !== confPwd) {
      e.preventDefault();
      alert('Passwords do not match. Please verify.');
      return;
    }
  });
}
