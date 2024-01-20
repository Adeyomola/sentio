const body = document.getElementById("body");

const buttons = [
  "bold",
  "italic",
  "underline",
  "justifyCenter",
  "justifyLeft",
  "justifyRight",
  "insertUnorderedList",
  "insertOrderedList",
  "redo",
  "undo",
  "strikeThrough",
  "subscript",
  "superscript",
  "createLink",
];

buttons.forEach((element) => {
  let command = element;
  if (element === "createLink") {
    let link = "https://";
    element = document.getElementById(element);
    element.onclick = () => document.execCommand(command, false, link);
  } else {
    element = document.getElementById(element);
    element.onclick = () => document.execCommand(command);
  }
});
