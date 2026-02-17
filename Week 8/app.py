import streamlit as st
import pandas as pd
import joblib

model = joblib.load("rf_energy_model.pkl")

st.set_page_config(page_title="Energy Predictor", layout="centered")

st.title("Next Hour Energy Consumption Predictor")
st.write("Provide building conditions to estimate next hour energy usage.")


temperature = st.number_input("Temperature (°C)", min_value=0.0, max_value=50.0, value=25.0)
humidity = st.number_input("Humidity (%)", min_value=0.0, max_value=100.0, value=50.0)
square_footage = st.number_input("Square Footage", min_value=100.0, value=1500.0)
occupancy = st.number_input("Current Occupancy", min_value=0, value=5)

hvac_input = st.radio("Is HVAC currently ON?", ["Yes", "No"])
lighting_input = st.radio("Are lights currently ON?", ["Yes", "No"])
holiday_input = st.radio("Is today a holiday?", ["Yes", "No"])

renewable = st.number_input("Renewable Energy Contribution", min_value=0.0, value=5.0)

# hour = st.slider("Hour of Day", 0, 23, 12)
hour = st.number_input("Hour of Day", min_value=0, max_value=23, value=12)

day = st.selectbox(
    "Day of Week",
    ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
)


hvac = 1 if hvac_input == "Yes" else 0
lighting = 1 if lighting_input == "Yes" else 0
holiday = 1 if holiday_input == "Yes" else 0

day_mapping = {
    "Monday": 0,
    "Tuesday": 1,
    "Wednesday": 2,
    "Thursday": 3,
    "Friday": 4,
    "Saturday": 5,
    "Sunday": 6
}

day_numeric = day_mapping[day]


expected_columns = model.feature_names_in_

if st.button("Predict Energy Consumption"):

    input_data = pd.DataFrame([[
        temperature,
        humidity,
        square_footage,
        occupancy,
        hvac,
        lighting,
        renewable,
        day_numeric,   
        holiday,
        hour            
    ]],
    columns=expected_columns) 

    prediction = model.predict(input_data)[0]

    st.success(f"Predicted Next Hour Energy Consumption: {prediction:.2f} units")
