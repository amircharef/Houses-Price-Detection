from pathlib import Path

import joblib
import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[1]
ARTIFACTS_DIR = BASE_DIR / "artifacts"
MODEL_PATH = ARTIFACTS_DIR / "house_price_model.joblib"


class ModelService:
    def __init__(self) -> None:
        self.model = None

    def load(self) -> None:
        if not MODEL_PATH.exists():
            raise FileNotFoundError(
                "Model not found. Run `python train.py` from the backend folder first."
            )
        self.model = joblib.load(MODEL_PATH)

    def predict(self, features: dict) -> float:
        if self.model is None:
            self.load()

        row = pd.DataFrame([features])
        prediction = self.model.predict(row)[0]
        return float(prediction)


model_service = ModelService()
