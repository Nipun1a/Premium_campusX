import pandas as pd
from fastapi import FastAPI
from fastapi import HTTPException, status
from fastapi.middleware.cors import CORSMiddleware

try:
    from model.predict import MODEL_VERSION, predict_output
except ImportError:  # pragma: no cover - supports running from the repo root
    from models.model.predict import MODEL_VERSION, predict_output

try:
    from models.schema.user_input import UserInput
except ImportError:  # pragma: no cover - supports running from the models/ directory
    from schema.user_input import UserInput

try:
    from models.schema.prediction_response import PredictionResponse
except ImportError:  # pragma: no cover - supports running from the models/ directory
    from schema.prediction_response import PredictionResponse


app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (can be restricted to ["http://localhost:8501"] for Streamlit)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "Insurance Premium Prediction API"}

@app.get('/health')
def health_check():
    return {
        'status': "OK",
        'version': MODEL_VERSION
    }


@app.post("/predict", response_model=PredictionResponse, status_code=status.HTTP_200_OK)
def predict_premium(data: UserInput):

    User_input = pd.DataFrame([{
        "age": data.age,
        "weight": data.weight,
        "height": data.height,
        "income_lpa": data.income_lpa,
        "city": data.city,
        "smoker": data.smoker,
        "occupation": data.occupation,
        "bmi": data.bmi,
        "age_group": data.age_group,
        "lifestyle_risk": data.lifestyle_risk,
        "city_tier": data.city_tier,
    }])

    try:
        prediction = predict_output(User_input)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Prediction failed: {exc}",
        )

    if isinstance(prediction, dict):
        return prediction

    return {
        "predicted_category": str(prediction),
        "confidence": None,
        "class_probabilities": {},
    }
