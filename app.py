import streamlit as st
import numpy as np
import pickle
import os

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Insurance Cost Predictor",
    page_icon="💰",
    layout="wide"
)

# ---------------- LOAD MODEL SAFELY ----------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(BASE_DIR, "Final_model_insurance.pkl")

try:
    with open(model_path, "rb") as f:
        model = pickle.load(f)
except FileNotFoundError:
    st.error("❌ Model file not found! Make sure 'Final_model_insurance.pkl' is in same folder.")
    st.stop()

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap');

html, body, [class*="css"]  {
    font-family: 'Poppins', sans-serif;
}

div.stButton > button {
    width: 100%;
    border-radius: 12px;
    height: 50px;
    font-size: 18px;
    font-weight: 600;
    transition: 0.3s;
}

div.stButton > button:hover {
    transform: scale(1.05);
}

@media (max-width: 768px) {
    .main-card {
        padding: 15px;
    }
}
</style>
""", unsafe_allow_html=True)

# ---------------- TITLE ----------------
st.markdown("<h1 style='text-align:center;'>💰 Insurance Cost Prediction</h1>", unsafe_allow_html=True)
st.write("")

col1, col2 = st.columns(2)

# ---------------- INPUTS ----------------
with col1:
    age = st.slider("Age", 18, 65, 25)
    sex = st.selectbox("Sex", ["male", "female"])
    bmi = st.slider("BMI", 15.0, 45.0, 25.0)
    children = st.slider("Number of Children", 0, 5, 0)
    smoker = st.selectbox("Smoker", ["yes", "no"])

with col2:
    region = st.selectbox("Region", ["northeast", "northwest", "southeast", "southwest"])
    annual_income = st.number_input("Annual Income (₹)", 200000, 1000000, 300000)
    exercise_frequency = st.slider("Exercise Days / Week", 0, 6, 3)

st.write("")

# ---------------- HEALTH DROPDOWN ----------------
st.subheader("🏥 Health Information")

health_issues = st.multiselect(
    "Select Health Problems",
    ["Diabetes", "High BP", "Heart Disease", "Asthma", "No major issues"]
)

# ---------------- MEDICAL SCORE CALCULATION ----------------
medical_history_score = 0

if "Diabetes" in health_issues:
    medical_history_score += 3
if "High BP" in health_issues:
    medical_history_score += 2
if "Heart Disease" in health_issues:
    medical_history_score += 4
if "Asthma" in health_issues:
    medical_history_score += 2

if "No major issues" in health_issues:
    medical_history_score = 0

# Extra risk logic (optional realistic touch)
if bmi > 30:
    medical_history_score += 2

if age > 50:
    medical_history_score += 1

if smoker == "yes":
    medical_history_score += 3

st.write(f"🩺 Calculated Medical Risk Score: {medical_history_score}")

# ---------------- ENCODING ----------------
sex = 1 if sex == "male" else 0
smoker = 1 if smoker == "yes" else 0

region_dict = {
    "northeast": 0,
    "northwest": 1,
    "southeast": 2,
    "southwest": 3
}
region = region_dict[region]

# ---------------- PREDICTION ----------------
if st.button("Predict Insurance Cost"):
    try:
        input_data = np.array([[age, sex, bmi, children, smoker,
                                region, medical_history_score,
                                annual_income, exercise_frequency]])

        prediction = model.predict(input_data)[0]

        st.success(f"✅ Predicted Insurance Cost: ₹ {prediction:,.2f}")

    except Exception as e:
        st.error(f"Prediction Error: {e}")
