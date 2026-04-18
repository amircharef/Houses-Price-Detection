from pydantic import BaseModel, Field


class HouseFeatures(BaseModel):
    area_m2: float = Field(..., gt=10, lt=10000)
    bedrooms: int = Field(..., ge=0, le=20)
    bathrooms: int = Field(..., ge=0, le=20)
    floors: int = Field(..., ge=1, le=10)
    age_years: int = Field(..., ge=0, le=300)
    distance_to_center_km: float = Field(..., ge=0, le=200)
    has_garage: int = Field(..., ge=0, le=1)
    has_garden: int = Field(..., ge=0, le=1)
    neighborhood_score: float = Field(..., ge=1, le=10)


class PredictionResponse(BaseModel):
    predicted_price: float
    currency: str = "DZA"
