import pandas as pd
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi import status

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
        return JSONResponse(
            status_code=400,
            content={"error": f"Prediction failed: {exc}"},
        )

    # `prediction` may be a dict with details (predicted_category, confidence, class_probabilities)
    if isinstance(prediction, dict):
        content = {"predicted_category": prediction}
    else:
        content = {"predicted_category": {"predicted_category": str(prediction)}}

    return JSONResponse(status_code=200, content=content)
