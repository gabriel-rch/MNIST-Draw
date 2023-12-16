const canvas = document.getElementById("drawing-board");
const clearButton = document.getElementById("clear-button");
const predictButton = document.getElementById("predict-button");
const context = canvas.getContext("2d");

const predict = async () => {
  const dataUrl = canvas.toDataURL();

  fetch("/predict", {
    method: "POST",
    body: JSON.stringify({ image: dataUrl }),
    headers: { "Content-Type": "application/json" },
  }).then((response) => {
    response.json().then((data) => {
      console.log(data);
      document.getElementById("prediction").innerHTML = data.label;
      document.getElementById("confidence").innerHTML =
        data.confidence.toFixed(2) * 100 + "% de confiança";
    });
  });
};

const clear = () => {
  context.clearRect(0, 0, canvas.width, canvas.height);
  for (let i = 0; i < 2; i++) {
    context.rect(0, 0, canvas.width, canvas.height);
    context.fill();
  }
  document.getElementById("prediction").innerHTML = "";
  document.getElementById("confidence").innerHTML = "";
};

context.lineCap = "round";
context.fillStyle = "#000000";
context.strokeStyle = "#FBFBFB";

context.rect(0, 0, canvas.width, canvas.height);
context.fill();

const strokeWidth = 20;

let drawing = false;

canvas.addEventListener("mousedown", () => {
  clear();
  drawing = true;
  context.beginPath();
  context.lineWidth = strokeWidth;
});

canvas.addEventListener("mouseup", () => {
  drawing = false;
  predict();
});

canvas.addEventListener("mousemove", (evt) => {
  if (!drawing) return;

  context.lineTo(evt.offsetX, evt.offsetY);
  context.stroke();
});

canvas.addEventListener("mouseout", () => {
  drawing = false;
});

clearButton.addEventListener("click", clear);
predictButton.addEventListener("click", predict);
