const ratingFields = [
  "Inflight wifi service",
  "Departure/Arrival time convenient",
  "Ease of Online booking",
  "Gate location",
  "Food and drink",
  "Online boarding",
  "Seat comfort",
  "Inflight entertainment",
  "On-board service",
  "Leg room service",
  "Baggage handling",
  "Checkin service",
  "Inflight service",
  "Cleanliness",
];

const example = {
  Gender: "Female",
  "Customer Type": "Loyal Customer",
  Age: 36,
  "Type of Travel": "Business travel",
  Class: "Business",
  "Flight Distance": 2863,
  "Departure Delay in Minutes": 0,
  "Arrival Delay in Minutes": 0,
  "Inflight wifi service": 4,
  "Departure/Arrival time convenient": 4,
  "Ease of Online booking": 4,
  "Gate location": 3,
  "Food and drink": 5,
  "Online boarding": 5,
  "Seat comfort": 5,
  "Inflight entertainment": 5,
  "On-board service": 5,
  "Leg room service": 5,
  "Baggage handling": 5,
  "Checkin service": 4,
  "Inflight service": 5,
  Cleanliness: 5,
};

const form = document.querySelector("#prediction-form");
const ratingsGrid = document.querySelector("#ratings-grid");
const resultTitle = document.querySelector("#result-title");
const resultDescription = document.querySelector("#result-description");
const probability = document.querySelector("#probability");
const drift = document.querySelector("#drift");
const meterFill = document.querySelector("#meter-fill");
const statusDot = document.querySelector(".status-dot");

function createRatingControls() {
  ratingFields.forEach((name) => {
    const label = document.createElement("label");
    label.textContent = name;

    const select = document.createElement("select");
    select.name = name;

    for (let value = 0; value <= 5; value += 1) {
      const option = document.createElement("option");
      option.value = value;
      option.textContent = value;
      if (value === 4) option.selected = true;
      select.appendChild(option);
    }

    label.appendChild(select);
    ratingsGrid.appendChild(label);
  });
}

function formToPayload() {
  const data = new FormData(form);
  const payload = {};

  for (const [key, value] of data.entries()) {
    const field = form.elements[key];
    payload[key] = field.type === "number" || field.tagName === "SELECT"
      ? coerceValue(value)
      : value;
  }

  return payload;
}

function coerceValue(value) {
  if (value !== "" && !Number.isNaN(Number(value))) {
    return Number(value);
  }
  return value;
}

function fillExample() {
  Object.entries(example).forEach(([key, value]) => {
    const element = form.elements[key];
    if (element) element.value = value;
  });
}

async function submitPrediction(event) {
  event.preventDefault();
  resultTitle.textContent = "Liczenie predykcji...";
  resultDescription.textContent = "Wysyłam dane do API modelu.";

  try {
    const response = await fetch("/predict", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(formToPayload()),
    });

    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.detail || "Nie udało się wykonać predykcji.");
    }

    renderResult(data);
  } catch (error) {
    resultTitle.textContent = "Brak wyniku";
    resultDescription.textContent = error.message;
    probability.textContent = "-";
    drift.textContent = "-";
    meterFill.style.width = "0%";
    statusDot.classList.remove("is-positive");
  }
}

function renderResult(data) {
  const prediction = data.prediction;
  const isSatisfied = prediction.prediction === "satisfied";
  const satisfiedProbability = prediction.probability_satisfied;
  const percent = Math.round(satisfiedProbability * 100);

  resultTitle.textContent = isSatisfied
    ? "Pasażer prawdopodobnie będzie zadowolony"
    : "Pasażer może być neutralny lub niezadowolony";
  resultDescription.textContent = prediction.interpretation;
  probability.textContent = `${percent}%`;
  drift.textContent = data.drift.status;
  meterFill.style.width = `${percent}%`;
  statusDot.classList.toggle("is-positive", isSatisfied);
}

createRatingControls();
fillExample();
form.addEventListener("submit", submitPrediction);
document.querySelector("#fill-example").addEventListener("click", fillExample);
