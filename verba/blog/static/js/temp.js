const body = document.getElementById("body");

// create popup for hyperlink
const linkPopUp = document.createElement("div");
linkPopUp.style.cssText = `position: fixed; transform: translate(2.5rem, 15rem);
  font: 0.7rem 'Nunito'; z-index: 5; 
  background-color: #1d242c1a; 
  padding: 0.5rem; border-radius: 0.1rem;`;
linkPopUp.innerText = "Enter a URL: ";
const link = document.createElement("input");
linkPopUp.appendChild(link);

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

function restoreSelection() {
  let range = document.createRange();

  range.setStart(body.firstChild, start);
  range.setEnd(body.lastChild, end);

  selection.removeAllRanges();
  selection.addRange(range);
}

buttons.forEach((element) => {
  let command = element;

  if (element === "createLink") {
    body.addEventListener("mouseout", preserveSelection);
    body.addEventListener("touchend", preserveSelection);
    element = document.getElementById(element);

    element.onclick = () => {
      if (window.getSelection().toString() == "" || link.value == null) return;
      document.body.appendChild(linkPopUp);
      link.focus();
      link.addEventListener("keyup", (e) => {
        if (e.key === "Enter") {
          restoreSelection();
          document.execCommand(command, false, link.value);
          link.value = "";
          document.body.removeChild(linkPopUp);
        }
      });
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
