const elementStrings = [
  "changedetails",
  "changepassword",
  "changedetailsForm",
  "changepasswordForm",
];

const elements = elementStrings.map((element) => {
  element = document.getElementById(element);
  return element;
});

const changedetails = elements[0];
const changepassword = elements[1];
const changedetailsForm = elements[2];
const changepasswordForm = elements[3];

changedetails.addEventListener("click", () => {
  changedetailsForm.style.display = "flex";
  changepasswordForm.style.display = "none";
});

changepassword.addEventListener("click", () => {
  changepasswordForm.style.display = "flex";
  changedetailsForm.style.display = "none";
});
