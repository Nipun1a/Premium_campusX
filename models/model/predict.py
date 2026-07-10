import pickle
from pathlib import Path

import pandas as pd


MODEL_PATH = Path(__file__).resolve().parent / "model.pkl"

if not MODEL_PATH.exists():
    raise FileNotFoundError(f"Model file not found at {MODEL_PATH}")

with MODEL_PATH.open("rb") as f:
    model = pickle.load(f)

MODEL_VERSION = "1.0.0"


def predict_output(user_input):
    if isinstance(user_input, dict):
        input_df = pd.DataFrame([user_input])
    elif isinstance(user_input, pd.DataFrame):
        input_df = user_input.copy()
    else:
        input_df = pd.DataFrame(user_input)

    if "city_tier" in input_df.columns and "city_tiers" not in input_df.columns:
        input_df = input_df.rename(columns={"city_tier": "city_tiers"})
    # Try to return class probabilities and confidence when available
    try:
        probs = model.predict_proba(input_df)[0]
        classes = list(getattr(model, "classes_", []))
        # Map class label -> probability
        class_probabilities = {str(classes[i]): float(probs[i]) for i in range(len(classes))}
        # Select predicted class and its confidence
        top_idx = int(probs.argmax()) if hasattr(probs, "argmax") else max(range(len(probs)), key=lambda i: probs[i])
        predicted = classes[top_idx] if classes else model.predict(input_df)[0]
        confidence = float(probs[top_idx])
    except Exception:
        # Fallback when predict_proba or classes_ not available
        predicted = model.predict(input_df)[0]
        class_probabilities = {}
        confidence = None

    return {
        "predicted_category": str(predicted),
        "confidence": confidence,
        "class_probabilities": class_probabilities,
    }