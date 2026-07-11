import requests
import streamlit as st


DEFAULT_API_URL = "http://127.0.0.1:8000/predict"


st.set_page_config(
    page_title="Insurance Premium Predictor",
    page_icon="Money",
    layout="wide",
)

st.markdown(
    """
    <style>
        .block-container {
            max-width: 1100px;
            padding-top: 2rem;
            padding-bottom: 2rem;
        }
        .hero {
            padding: 1.5rem 1.75rem;
            border-radius: 20px;
            background: linear-gradient(135deg, #102a43 0%, #1f6f78 100%);
            color: white;
            margin-bottom: 1.5rem;
        }
        .hero h1 {
            margin: 0;
            font-size: 2.25rem;
        }
        .hero p {
            margin: 0.5rem 0 0 0;
            opacity: 0.92;
            font-size: 1rem;
        }
        .result-card {
            padding: 1.25rem 1.5rem;
            border-radius: 16px;
            border: 1px solid rgba(16, 42, 67, 0.12);
            background: #f8fbfd;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


st.markdown(
    """
    <div class="hero">
        <h1>Insurance Premium Predictor</h1>
        <p>Enter a few health and lifestyle details to predict the premium category.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

api_url = DEFAULT_API_URL

with st.form("prediction_form"):
    left, right = st.columns(2)

    with left:
        age = st.number_input("Age", min_value=1, max_value=120, value=25)
        weight = st.number_input("Weight (kg)", min_value=20.0, max_value=150.0, value=70.0)
        height = st.number_input("Height (meters)", min_value=0.5, max_value=2.5, value=1.75, step=0.01)
        income = st.number_input("Income (LPA)", min_value=0.0, max_value=120.0, value=5.0)

    with right:
        cities = [
            "Mumbai",
            "Delhi",
            "Bangalore",
            "Chennai",
            "Kolkata",
            "Hyderabad",
            "Pune",
            "Jaipur",
            "Lucknow",
            "Noida",
            "Indore",
            "Surat",
            "Patna",
            "Ranchi",
        ]
        city = st.selectbox("City", cities)
        occupation = st.selectbox(
            "Occupation",
            [
                "student",
                "private_job",
                "government_job",
                "business_owner",
                "freelancer",
                "retired",
                "unemployed",
            ],
        )
        smoker = st.radio("Smoker", ["No", "Yes"], horizontal=True)

    submitted = st.form_submit_button("Predict Premium")


if submitted:
    payload = {
        "age": int(age),
        "weight": float(weight),
        "height": float(height),
        "income_lpa": float(income),
        "city": city,
        "smoker": smoker == "Yes",
        "occupation": occupation,
    }

    try:
        response = requests.post(api_url, json=payload, timeout=15)
        response.raise_for_status()
        result = response.json()

        if isinstance(result, dict) and isinstance(result.get("predicted_category"), dict):
            result = result["predicted_category"]

        prediction = result.get("predicted_category", "Unknown")
        confidence = result.get("confidence")
        class_probs = result.get("class_probabilities", {}) or {}

        st.markdown('<div class="result-card">', unsafe_allow_html=True)
        st.subheader("Prediction Result")
        st.success(f"Predicted Premium Category: {prediction}")

        if confidence is not None:
            st.write(f"Confidence: **{confidence:.2%}**")

        if class_probs:
            st.write("Class Probabilities")
            st.bar_chart(class_probs)

        st.markdown("</div>", unsafe_allow_html=True)

    except requests.exceptions.ConnectionError as exc:
        st.error(
            "Unable to connect to FastAPI Server.\n\n"
            f"{exc}\n\n"
            "Start the API first, usually with something like:\n"
            "`uvicorn app:app --reload` from the `models` folder."
        )
    except requests.exceptions.HTTPError as exc:
        error_body = response.text if "response" in locals() else str(exc)
        st.error(f"FastAPI returned an error.\n\n{error_body}")
    except Exception as exc:
        st.error(f"Unexpected frontend error.\n\n{exc}")
