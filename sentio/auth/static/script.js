const password = document.getElementById("password");
const confirm_password = document.getElementById("confirm_password");

function validatePassword(e) {
  if (password.value != confirm_password.value) {
    confirm_password.setCustomValidity("Passwords do not match");
    confirm_password.reportValidity();
    e.preventDefault();
  } else {
    confirm_password.setCustomValidity("");
  }
}

password.onchange = validatePassword;
confirm_password.onkeyup = validatePassword;
