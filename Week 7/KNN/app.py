import streamlit as st
import pandas as pd
import joblib

# -----------------------------
# Load Model
# -----------------------------
model = joblib.load("knn_income_model.pkl")

st.set_page_config(page_title="Adult Income Predictor", layout="centered")

st.title("📊 Adult Census Income Prediction")
st.write("Predict whether an individual earns more than $50K annually.")

st.divider()

# =============================
# Personal Information
# =============================
st.subheader("👤 Personal Information")
age = st.number_input(
    "Age",
    min_value=17,
    max_value=90,
    value=30,
    step=1
)

education_mapping = {
    "Preschool": 1,
    "1st-4th": 2,
    "5th-6th": 3,
    "7th-8th": 4,
    "9th": 5,
    "10th": 6,
    "11th": 7,
    "12th": 8,
    "HS-grad": 9,
    "Some-college": 10,
    "Assoc-voc": 11,
    "Assoc-acdm": 12,
    "Bachelors": 13,
    "Masters": 14,
    "Prof-school": 15,
    "Doctorate": 16
}

education = st.selectbox("Highest Education Level", list(education_mapping.keys()))
educational_num = education_mapping[education]


marital_status = st.selectbox("Marital Status", [
    "Never-married", "Married-civ-spouse", "Divorced",
    "Separated", "Widowed", "Married-spouse-absent", "Married-AF-spouse"
])

relationship = st.selectbox("Relationship Status", [
    "Husband", "Wife", "Own-child", 
    "Not-in-family", "Other-relative", "Unmarried"
])

gender = st.selectbox("Gender", ["Male", "Female"])

race = st.selectbox("Race", [
    "White", "Black", "Asian-Pac-Islander",
    "Amer-Indian-Eskimo", "Other"
])

native_country = st.selectbox("Native Country", [
    "United-States", "India", "Mexico", "Philippines",
    "Germany", "Canada", "China", "England", "Cuba", "South"
])

st.divider()

# =============================
# Employment Information
# =============================
st.subheader("💼 Employment Information")

workclass = st.selectbox("Workclass", [
    "Private", "Self-emp-not-inc", "Self-emp-inc",
    "Federal-gov", "Local-gov", "State-gov",
    "Without-pay", "Never-worked"
])

occupation = st.selectbox("Occupation", [
    "Tech-support", "Craft-repair", "Other-service", "Sales",
    "Exec-managerial", "Prof-specialty", "Handlers-cleaners",
    "Machine-op-inspct", "Adm-clerical", "Farming-fishing",
    "Transport-moving", "Priv-house-serv",
    "Protective-serv", "Armed-Forces"
])

hours_per_week = st.number_input(
    "hours-per-week",
    min_value=1,
    max_value=100,
    value=40,
    step=1
)
capital_gain = st.number_input("Capital Gain ($)", min_value=0, value=0)
capital_loss = st.number_input("Capital Loss ($)", min_value=0, value=0)

st.divider()

# =============================
# Prediction
# =============================
if st.button("🔍 Predict Income Category"):

    input_data = pd.DataFrame({
        "age": [age],
        "educational-num": [educational_num],  # Hidden but required
        "capital-gain": [capital_gain],
        "capital-loss": [capital_loss],
        "hours-per-week": [hours_per_week],
        "workclass": [workclass],
        "education": [education],
        "marital-status": [marital_status],
        "occupation": [occupation],
        "relationship": [relationship],
        "race": [race],
        "gender": [gender],
        "native-country": [native_country]
    })

    prediction = model.predict(input_data)[0]
    probability = model.predict_proba(input_data)[0]

    st.subheader("📌 Prediction Result")

    if prediction == 1:
        st.success("Estimated Income: > $50K")
    else:
        st.info("Estimated Income: ≤ $50K")

    st.write(f"Confidence Level: {round(max(probability)*100, 2)}%")
