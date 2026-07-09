import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/predict"

st.set_page_config(
    page_title="Insurance Premium Predictor",
    page_icon="💰",
    layout="centered"
)

st.title("💰 Insurance Premium Predictor")

st.write("Enter your details to predict your insurance premium category.")

age = st.number_input(
    "Age",
    min_value=1,
    max_value=120,
    value=25
)

weight = st.number_input(
    "Weight (kg)",
    min_value=20.0,
    max_value=150.0,
    value=70.0
)

height = st.number_input(
    "Height (meters)",
    min_value=0.5,
    max_value=2.5,
    value=1.75,
    step=0.01
)

income = st.number_input(
    "Income (LPA)",
    min_value=0.0,
    max_value=100.0,
    value=5.0
)

cities = [
    "Mumbai","Delhi","Bangalore","Chennai","Kolkata",
    "Hyderabad","Pune","Jaipur","Lucknow","Noida",
    "Indore","Surat","Patna","Ranchi"
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
        "unemployed"
    ]
)

smoker = st.radio(
    "Smoker",
    ["No", "Yes"]
)

if st.button("Predict Premium"):

    payload = {
        "age": age,
        "weight": weight,
        "height": height,
        "income_lpa": income,
        "city": city,
        "smoker": smoker == "Yes",
        "occupation": occupation
    }

    try:
        response = requests.post(API_URL, json=payload)

        if response.status_code == 200:

            prediction = response.json()["predicted_category"]

            st.success(f"Predicted Premium Category: **{prediction}**")

        else:
            st.error(response.json())

    except Exception as e:
        st.error(f"Unable to connect to FastAPI Server.\n\n{e}")