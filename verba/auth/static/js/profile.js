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

elements[0].addEventListener("click", () => {
  elements[0].style.color = "lightskyblue";
  elements[1].style.color = "";
  elements[2].style.display = "flex";
  elements[3].style.display = "none";
});

elements[1].addEventListener("click", () => {
  elements[0].style.color = "#1d242c";
  elements[2].style.display = "none";
  elements[1].style.color = "lightskyblue";
  elements[3].style.display = "flex";
});
