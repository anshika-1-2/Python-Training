import streamlit as st
import numpy as np
import joblib

# Load model and scaler
model = joblib.load("ad_click_model.pkl")
scaler = joblib.load("scaler.pkl")

st.title("Ad Click Prediction System")

st.write("Enter user details below:")

# User Inputs
daily_time_spent = st.number_input("Daily Time Spent on Site", min_value=10.0)
age = st.number_input("Age", min_value=0)
area_income = st.number_input("Area Income", min_value=12000.0)
daily_internet_usage = st.number_input("Daily Internet Usage", min_value=100.0)
gender = st.selectbox("Gender", ["Female", "Male"])

# Convert gender
male = 1 if gender == "Male" else 0

# Predict Button
if st.button("Predict"):

    user_data = np.array([[daily_time_spent,
                           age,
                           area_income,
                           daily_internet_usage,
                           male]])

    user_scaled = scaler.transform(user_data)

    probability = model.predict_proba(user_scaled)[0][1]
    prediction = model.predict(user_scaled)[0]

    st.subheader("Result")

    if prediction == 1:
        st.success("User is likely to CLICK the ad.")
    else:
        st.error("User is NOT likely to click the ad.")

    st.write(f"Click Probability: {round(probability*100,2)}%")
