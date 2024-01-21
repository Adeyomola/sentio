const body = document.getElementById("body");

// get popup elements
const linkPopUp = document.getElementById("linkPopUp");
const link = document.getElementById("link");
const linkButton = document.getElementById("linkButton");

// array for editor buttons
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
  "unlink",
  "formatBlock",
];

// variables for selection preservation
let start;
let end;
let selection;

// gets selection offset be entering popup
function preserveSelection() {
  selection = window.getSelection();
  if (selection.anchorOffset < selection.focusOffset) {
    start = selection.anchorOffset;
    end = selection.focusOffset;
  } else {
    start = selection.focusOffset;
    end = selection.anchorOffset;
  }
}

// restores selection when we're leaving popup
function restoreSelection() {
  let range = document.createRange();

  range.setStart(body.firstChild, start);
  range.setEnd(body.lastChild, end);
  selection.removeAllRanges();
  selection.addRange(range);
}

// function that saves link entered in popup
function saveLink(command) {
  link.addEventListener("keyup", (e) => {
    if (e.key === "Enter") {
      restoreSelection();
      document.execCommand(command, false, link.value);
      link.value = "https://";
      linkPopUp.style.display = "none";
    }
  });
  linkButton.addEventListener("click", () => {
    restoreSelection();
    document.execCommand(command, false, link.value);
    link.value = "https://";
    linkPopUp.style.display = "none";
  });
}

// forEach loop that creates eventlisteners that execcommand for each editor button
buttons.forEach((element) => {
  let command = element;

  if (element === "createLink") {
    body.addEventListener("mouseout", preserveSelection);
    body.addEventListener("touchend", preserveSelection);
    element = document.getElementById(element);

    element.onclick = () => {
      if (window.getSelection().toString() == "") return;
      linkPopUp.style.display = "flex";
      link.focus();
      saveLink(command);
    };
  } else if (
    element === "insertUnorderedList" ||
    element === "insertOrderedList"
  ) {
    element = document.getElementById(element);
    element.onclick = () => {
      document.execCommand("indent");
      document.execCommand(command);
    };
  } else if (element === "formatBlock") {
    element = document.getElementById(element);
    element.onmouseup = (e) => {
      e.preventDefault();
      document.execCommand(command, false, element.value);
    };
    element.ontouchend = () => {
      e.preventDefault();
      document.execCommand(command, false, element.value);
    };
  } else {
    element = document.getElementById(element);
    element.onclick = () => document.execCommand(command);
  }
});
