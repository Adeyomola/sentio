const elementStrings = [
  "uploadProfilePicture",
  "changedetails",
  "changepassword",
  "uploadProfilePictureForm",
  "changedetailsForm",
  "changepasswordForm",
];

const elements = elementStrings.map((element) => {
  element = document.getElementById(element);
  return element;
});

elements[0].addEventListener("click", () => {
  elements[0].style.color = "lightskyblue";
  elements[1].style.color = "#1d242c";
  elements[2].style.color = "#1d242c";
  elements[3].style.display = "flex";
  elements[4].style.display = "none";
  elements[5].style.display = "none";
});

elements[1].addEventListener("click", () => {
  elements[0].style.color = "#1d242c";
  elements[1].style.color = "lightskyblue";
  elements[2].style.color = "#1d242c";
  elements[3].style.display = "none";
  elements[4].style.display = "flex";
  elements[5].style.display = "none";
});

elements[2].addEventListener("click", () => {
  elements[0].style.color = "#1d242c";
  elements[1].style.color = "#1d242c";
  elements[2].style.color = "lightskyblue";
  elements[3].style.display = "none";
  elements[4].style.display = "none";
  elements[5].style.display = "flex";
});
