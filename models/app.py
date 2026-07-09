from pathlib import Path
import pickle

import pandas as pd
from fastapi import FastAPI
from fastapi.responses import JSONResponse

try:
    from models.schema.user_input import UserInput
except ImportError:  # pragma: no cover - supports running from the models/ directory
    from schema.user_input import UserInput

# Load Model
MODEL_PATH = Path(__file__).parent / "model" / "model.pkl"

with MODEL_PATH.open("rb") as f:
    model = pickle.load(f)
 
 #in this it is hardcoded but it is came with the help of mlflow   
MODEL_VERSION = '1.0.0'
    
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


@app.post("/predict")
def predict_premium(data: UserInput):

    input_df = pd.DataFrame([{
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

    prediction = model.predict(input_df)[0]

    return JSONResponse(
        status_code=200,
        content={
            "predicted_category": str(prediction)
        }
    )
