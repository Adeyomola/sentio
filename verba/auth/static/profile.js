const changedetails = document.getElementById("changedetails");
const changepassword = document.getElementById("changepassword");
const changedetailsForm = document.getElementById("changedetailsForm");
const changepasswordForm = document.getElementById("changepasswordForm");

changedetails.addEventListener("click", () => {
  changedetailsForm.style.display = "flex";
  changepasswordForm.style.display = "none";
});

changepassword.addEventListener("click", () => {
  changepasswordForm.style.display = "flex";
  changedetailsForm.style.display = "none";
});
