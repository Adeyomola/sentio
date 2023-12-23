var password = document.getElementsByName("password"),
  confirm_password = document.getElementsByName("confirm_password");

function validatePassword() {
  if (password.value != confirm_password.value) {
    confirm_password.setCustomValidity("Passwords do not match");
  } else {
    confirm_password.setCustomValidity("");
  }
}

password.onchange = validatePassword;
confirm_password.onkeyup = validatePassword;
