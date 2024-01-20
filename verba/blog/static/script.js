const body = document.getElementById("body");
const bold = document.getElementById("bold");

let start;
let end;

body.addEventListener("select", getse);

function getse(e) {
  e.preventDefault();
  start = e.target.selectionStart;
  end = e.target.selectionEnd;
  boldText(start, end);
}

function boldText(start, end) {
  bold.addEventListener(
    "click",
    (e) => {
      e.preventDefault();

      let stringbefore = body.value.substring(0, start);
      let stringafter = body.value.substring(end, body.value.length);
      console.log(start, end);

      let target = body.value.substring(start, end).trim();
      target = `<b>${target}</b>`;

      let newbody = stringbefore + target + stringafter;
      body.value = newbody;
    },
    { once: true }
  );
}
