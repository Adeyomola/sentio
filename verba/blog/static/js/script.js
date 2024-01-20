const body = document.getElementById("body");
const bold = document.getElementById("bold");
const formatted = document.getElementById("formatted");

// body.addEventListener("keyup", () => {
//   formatted.innerHTML = body.value;
// });

let start;
let end;

formatted.addEventListener("mouseup" || "touchstart", getStartEnd);

function getStartEnd(e) {
  e.preventDefault();
  let target = window.getSelection();
  if (target.toString() == "") return;
  if (target.anchorOffset < target.focusOffset) {
    start = target.anchorOffset;
    end = target.focusOffset;
  } else {
    start = target.focusOffset;
    end = target.anchorOffset;
  }
  console.log([start, end, target]);
  console.log(formatted.innerText);
  boldText(start, end);
}

function boldText(start, end) {
  bold.addEventListener(
    "click",
    (e) => {
      e.preventDefault();

      let stringbefore = formatted.innerText.substring(0, start);
      let stringafter = formatted.innerText.substring(
        end,
        formatted.innerText.length
      );

      let target = formatted.innerText.substring(start, end);

      if (/<b>/.test(target) || /<\/b>/.test(target)) {
        target = target.replace(/<b>/g, "");
        target = target.replace(/<\/b>/g, "");
      } else {
        target = `<b>${target}</b>`;
      }

      let newbody = stringbefore + target + stringafter;
      formatted.innerHTML = newbody;
    },
    { once: true }
  );
}

// body.addEventListener("select", getStartEnd);

// function getStartEnd(e) {
//   e.preventDefault();
//   start = e.target.selectionStart;
//   end = e.target.selectionEnd;
//   boldText(start, end);
// }

// function boldText(start, end) {
//   bold.addEventListener(
//     "click",
//     (e) => {
//       e.preventDefault();

//       let stringbefore = body.value.substring(0, start);
//       let stringafter = body.value.substring(end, body.value.length);

//       let target = body.value.substring(start, end);

//       if (/<b>/.test(target) || /<\/b>/.test(target)) {
//         target = target.replace(/<b>/g, "");
//         target = target.replace(/<\/b>/g, "");
//       } else {
//         target = `<b>${target}</b>`;
//       }

//       let newbody = stringbefore + target + stringafter;
//       body.value = newbody;
//       formatted.innerHTML = body.value;
//     },
//     { once: true }
//   );
// }
