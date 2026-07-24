/**
 * User Profile client interactions
 */

document.addEventListener('DOMContentLoaded', () => {
  setupProfileBMICalculation();
  setupAvatarUploadMock();
});

/**
 * Recalculate BMI in real-time when height/weight are modified in the edit form
 */
function setupProfileBMICalculation() {
  const heightInput = document.getElementById('height');
  const weightInput = document.getElementById('weight');
  const bmiVal = document.getElementById('profile-bmi-val');

  if (!heightInput || !weightInput || !bmiVal) return;

  function recalculate() {
    const heightCm = parseFloat(heightInput.value);
    const weightKg = parseFloat(weightInput.value);

    if (heightCm > 50 && weightKg > 10) {
      const heightM = heightCm / 100.0;
      const bmi = weightKg / (heightM * heightM);
      bmiVal.textContent = bmi.toFixed(2);
    } else {
      bmiVal.textContent = '--';
    }
  }

  heightInput.addEventListener('input', recalculate);
  weightInput.addEventListener('input', recalculate);
}

/**
 * Handle simulated image uploading
 */
function setupAvatarUploadMock() {
  const uploadBtn = document.getElementById('upload-avatar-mock');
  if (!uploadBtn) return;

  uploadBtn.addEventListener('click', (e) => {
    e.preventDefault();
    alert('Profile picture uploads are simulated in this version. Your avatar remains as your initials.');
  });
}
