import json
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
ARTIFACTS_DIR = BASE_DIR / "artifacts"
DATA_PATH = DATA_DIR / "housing.csv"
MODEL_PATH = ARTIFACTS_DIR / "house_price_model.joblib"
METRICS_PATH = ARTIFACTS_DIR / "metrics.json"


def generate_demo_data(n_samples: int = 2000, seed: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(seed)

    area_m2 = rng.uniform(35, 400, n_samples)
    bedrooms = rng.integers(1, 7, n_samples)
    bathrooms = rng.integers(1, 5, n_samples)
    floors = rng.integers(1, 4, n_samples)
    age_years = rng.integers(0, 80, n_samples)
    distance_to_center_km = rng.uniform(0.5, 35, n_samples)
    has_garage = rng.integers(0, 2, n_samples)
    has_garden = rng.integers(0, 2, n_samples)
    neighborhood_score = rng.uniform(1, 10, n_samples)

    noise = rng.normal(0, 15000, n_samples)
    price = (
        area_m2 * 2200
        + bedrooms * 15000
        + bathrooms * 12000
        + floors * 9000
        - age_years * 1100
        - distance_to_center_km * 3200
        + has_garage * 18000
        + has_garden * 12000
        + neighborhood_score * 25000
        + noise
    )

    price = np.maximum(price, 30000)

    return pd.DataFrame(
        {
            "area_m2": area_m2,
            "bedrooms": bedrooms,
            "bathrooms": bathrooms,
            "floors": floors,
            "age_years": age_years,
            "distance_to_center_km": distance_to_center_km,
            "has_garage": has_garage,
            "has_garden": has_garden,
            "neighborhood_score": neighborhood_score,
            "price": price,
        }
    )


def load_dataset() -> pd.DataFrame:
    if DATA_PATH.exists():
        return pd.read_csv(DATA_PATH)

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    demo = generate_demo_data()
    demo.to_csv(DATA_PATH, index=False)
    return demo


def main() -> None:
    df = load_dataset()

    target_column = "price"
    feature_columns = [c for c in df.columns if c != target_column]

    X = df[feature_columns]
    y = df[target_column]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = RandomForestRegressor(
        n_estimators=400,
        max_depth=18,
        min_samples_split=4,
        random_state=42,
        n_jobs=-1,
    )
    model.fit(X_train, y_train)

    preds = model.predict(X_test)
    metrics = {
        "mae": float(mean_absolute_error(y_test, preds)),
        "r2": float(r2_score(y_test, preds)),
        "rows": int(len(df)),
    }

    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, MODEL_PATH)
    METRICS_PATH.write_text(json.dumps(metrics, indent=2), encoding="utf-8")

    print("Training complete")
    print(json.dumps(metrics, indent=2))
    print(f"Model saved to: {MODEL_PATH}")


if __name__ == "__main__":
    main()
