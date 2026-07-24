/**
 * Registration Page client-side interactions and real-time BMI calculations
 */

document.addEventListener('DOMContentLoaded', () => {
  setupBMICalculation();
  setupRegistrationValidation();
});

/**
 * Attaches event listeners to Height and Weight inputs to calculate BMI
 */
function setupBMICalculation() {
  const heightInput = document.getElementById('height');
  const weightInput = document.getElementById('weight');
  const bmiVal = document.getElementById('bmi-val');
  const bmiCat = document.getElementById('bmi-cat');

  if (!heightInput || !weightInput || !bmiVal || !bmiCat) return;

  function recalculate() {
    const heightCm = parseFloat(heightInput.value);
    const weightKg = parseFloat(weightInput.value);

    if (heightCm > 50 && weightKg > 10) {
      const heightM = heightCm / 100.0;
      const bmi = weightKg / (heightM * heightM);
      const bmiRounded = bmi.toFixed(2);
      
      bmiVal.textContent = bmiRounded;
      
      // Determine category
      if (bmi < 18.5) {
        bmiCat.textContent = 'Underweight';
        bmiCat.style.color = '#3b82f6'; // Blue
      } else if (bmi >= 18.5 && bmi < 25) {
        bmiCat.textContent = 'Normal weight';
        bmiCat.style.color = '#10b981'; // Mint/Green
      } else if (bmi >= 25 && bmi < 30) {
        bmiCat.textContent = 'Overweight';
        bmiCat.style.color = '#f59e0b'; // Orange
      } else {
        bmiCat.textContent = 'Obese';
        bmiCat.style.color = '#ef4444'; // Red
      }
    } else {
      bmiVal.textContent = '--';
      bmiCat.textContent = 'Enter weight & height';
      bmiCat.style.color = 'var(--text-secondary)';
    }
  }

  heightInput.addEventListener('input', recalculate);
  weightInput.addEventListener('input', recalculate);
}

/**
 * Validates signup fields (e.g. password confirm validation)
 */
function setupRegistrationValidation() {
  const form = document.getElementById('register-form');
  if (!form) return;

  form.addEventListener('submit', (e) => {
    const pwd = document.getElementById('password').value;
    const pwdConf = document.getElementById('confirm_password').value;

    if (pwd.length < 8) {
      e.preventDefault();
      alert('Password must be at least 8 characters long.');
      return;
    }

    if (pwd !== pwdConf) {
      e.preventDefault();
      alert('Passwords do not match. Please verify.');
      return;
    }
  });
}
