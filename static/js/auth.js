/**
 * Core Auth Form Validations & OAuth Mocks (Login Page)
 */

document.addEventListener('DOMContentLoaded', () => {
  setupLoginForm();
  setupGoogleSignin();
});

function setupLoginForm() {
  const loginForm = document.getElementById('login-form');
  if (!loginForm) return;

  loginForm.addEventListener('submit', (e) => {
    const email = document.getElementById('email').value.trim();
    const password = document.getElementById('password').value;

    if (!email || !password) {
      e.preventDefault();
      alert('Please fill out all fields.');
      return;
    }
  });

  const forgotTrigger = document.getElementById('forgot-password-trigger');
  if (forgotTrigger) {
    forgotTrigger.addEventListener('click', (e) => {
      e.preventDefault();
      alert('Password reset instructions have been simulated. Check your inbox!');
    });
  }
}

function setupGoogleSignin() {
  const googleBtn = document.getElementById('google-signin-btn');
  if (!googleBtn) return;

  googleBtn.addEventListener('click', (e) => {
    e.preventDefault();
    alert('Google Login is currently simulated. Please use standard email login.');
  });
}
