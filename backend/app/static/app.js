const form = document.getElementById("predictForm");
const resultEl = document.getElementById("result");

function parseForm(formData) {
  return {
    area_m2: Number(formData.get("area_m2")),
    bedrooms: Number(formData.get("bedrooms")),
    bathrooms: Number(formData.get("bathrooms")),
    floors: Number(formData.get("floors")),
    age_years: Number(formData.get("age_years")),
    distance_to_center_km: Number(formData.get("distance_to_center_km")),
    has_garage: Number(formData.get("has_garage")),
    has_garden: Number(formData.get("has_garden")),
    neighborhood_score: Number(formData.get("neighborhood_score")),
  };
}

function asCurrency(value) {
  return new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: "USD",
    maximumFractionDigits: 0,
  }).format(value);
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  resultEl.textContent = "Predicting...";

  const payload = parseForm(new FormData(form));

  try {
    const response = await fetch("/predict", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || "Prediction request failed.");
    }

    const data = await response.json();
    resultEl.textContent = `Estimated house price: ${asCurrency(data.predicted_price)}`;
  } catch (error) {
    resultEl.textContent = `Error: ${error.message}`;
  }
});
