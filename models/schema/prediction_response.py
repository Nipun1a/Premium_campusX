from typing import Dict, Optional

from pydantic import BaseModel, Field


class PredictedDetail(BaseModel):
    predicted_category: str = Field(..., description="Predicted label/category")
    confidence: Optional[float] = Field(
        None, description="Confidence score between 0 and 1 (if available)"
    )
    class_probabilities: Dict[str, float] = Field(
        default_factory=dict, description="Per-class probabilities"
    )

    class Config:
        schema_extra = {
            "example": {
                "predicted_category": "Low",
                "confidence": 0.39,
                "class_probabilities": {"High": 0.36, "Low": 0.39, "Medium": 0.25},
            }
        }


class PredictionResponse(BaseModel):
    predicted_category: PredictedDetail

    class Config:
        schema_extra = {
            "example": {
                "predicted_category": {
                    "predicted_category": "Low",
                    "confidence": 0.39,
                    "class_probabilities": {"High": 0.36, "Low": 0.39, "Medium": 0.25},
                }
            }
        }
