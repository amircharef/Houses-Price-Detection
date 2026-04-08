# Houses-Price-Detection

End-to-end AI project to predict house prices from property features.

This repository now includes:

- A Python training pipeline (`scikit-learn`) to create a house-price model.
- A FastAPI backend with a `/predict` endpoint.
- A responsive web interface where users submit house features and get an instant prediction.
- A Google Colab notebook for training the model and running a Colab-friendly demo UI.

## Project Structure

```text
backend/
	app/
		__init__.py
		main.py
		model_service.py
		schemas.py
		static/
			index.html
			styles.css
			app.js
	artifacts/              # model and metrics generated after training
	data/                   # training CSV (auto-generated demo dataset if missing)
	requirements.txt
	train.py
README.md
```

## 1) Setup Environment

From the repository root:

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## 2) Train the Model

```powershell
python train.py
```

What this does:

- Uses `backend/data/housing.csv` if it exists.
- Otherwise auto-generates a demo dataset and saves it.
- Trains a `RandomForestRegressor` model.
- Saves the model to `backend/artifacts/house_price_model.joblib`.
- Saves basic metrics to `backend/artifacts/metrics.json`.

## 3) Run the API + Web App

```powershell
uvicorn app.main:app --reload
```

Open:

- http://127.0.0.1:8000

API endpoints:

- `GET /health`
- `POST /predict`

## 4) Example Prediction Request

```json
{
  "area_m2": 180,
  "bedrooms": 4,
  "bathrooms": 3,
  "floors": 2,
  "age_years": 12,
  "distance_to_center_km": 6.5,
  "has_garage": 1,
  "has_garden": 1,
  "neighborhood_score": 8.4
}
```

## Notes

- The current training pipeline is fully functional and meant as a strong starter.
- For production quality, replace the demo dataset with your real housing data in `backend/data/housing.csv` using the same column names.
- The web UI is responsive and works on desktop, tablet, and mobile browsers.

## Google Colab

Use [colab/house_price_colab.ipynb](colab/house_price_colab.ipynb) if you want to run the project inside Google Colab.

The notebook includes:

- Runtime and Python checks.
- Dependency installation.
- Three loading options: upload files, mount Google Drive, or clone the GitHub repo.
- Colab-safe paths and persistence to Google Drive.
- Training the model end-to-end.
- A lightweight Gradio interface for prediction in Colab.
