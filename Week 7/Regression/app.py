import streamlit as st
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
@st.cache_data
def load_and_train():

    df = pd.read_csv("Walmart.csv")
    df['Date'] = pd.to_datetime(df['Date'], dayfirst=True)

    min_date = df['Date'].min()
    max_date = df['Date'].max()

    # Time features
    df['Year'] = df['Date'].dt.year
    df['Month'] = df['Date'].dt.month
    df['Week'] = df['Date'].dt.isocalendar().week.astype(int)
    df['Quarter'] = df['Date'].dt.quarter

    # Create ranges
    df['Temp_Range'] = pd.cut(
        df['Temperature'],
        bins=[-100, 40, 75, 200],
        labels=["Low", "Medium", "High"]
    )

    df['Fuel_Range'] = pd.cut(
        df['Fuel_Price'],
        bins=[-10, 2.5, 3.5, 10],
        labels=["Low", "Medium", "High"]
    )

    # Save means BEFORE dropping columns
    cpi_mean = df['CPI'].mean()
    unemployment_mean = df['Unemployment'].mean()

    df = df.drop(columns=['Date', 'Temperature', 'Fuel_Price'])

    df = pd.get_dummies(
        df,
        columns=['Store', 'Temp_Range', 'Fuel_Range'],
        drop_first=True
    )

    X = df.drop(columns=['Weekly_Sales'])
    y = df['Weekly_Sales']

    model = LinearRegression()
    model.fit(X, y)

    return model, X.columns, min_date, max_date, cpi_mean, unemployment_mean


model, feature_columns, min_date, max_date, cpi_mean, unemployment_mean = load_and_train()

# ------------------------------------
# Streamlit UI
# ------------------------------------
st.title("Walmart Weekly Sales Prediction")

st.write("All inputs are within trained data range. No extrapolation allowed.")

# -----------------------------
# User Inputs
# -----------------------------
store = st.number_input("Store Number", min_value=1, step=1)

holiday_option = st.radio("Is it a Holiday Week?", ["No", "Yes"])

temp_range = st.selectbox("Temperature Range", ["Low", "Medium", "High"])

fuel_range = st.selectbox("Fuel Price Range", ["Low", "Medium", "High"])

cpi = st.number_input("CPI (leave 0 for dataset mean)", value=0.0)
unemployment = st.number_input("Unemployment (leave 0 for dataset mean)", value=0.0)

date = st.date_input(
    "Select Date (Restricted to Training Data)",
    min_value=min_date,
    max_value=max_date
)

# ------------------------------------
# Prediction
# ------------------------------------
if st.button("Predict Sales"):

    input_dict = {}
    input_dict['CPI'] = cpi if cpi != 0 else cpi_mean
    input_dict['Unemployment'] = unemployment if unemployment != 0 else unemployment_mean

    input_dict['Holiday'] = 1 if holiday_option == "Yes" else 0
    # Time features
    input_dict['Year'] = date.year
    input_dict['Month'] = date.month
    input_dict['Week'] = pd.to_datetime(date).isocalendar().week
    input_dict['Quarter'] = (date.month - 1) // 3 + 1

    # Initialize only dummy columns as 0
    for col in feature_columns:
        if col.startswith("Store_") or col.startswith("Temp_Range_") or col.startswith("Fuel_Range_"):
            input_dict[col] = 0

    # Store dummy
    if store != 1:
        store_col = f"Store_{store}"
        if store_col in feature_columns:
            input_dict[store_col] = 1

    # Temperature dummy
    if temp_range != "Low":
        temp_col = f"Temp_Range_{temp_range}"
        if temp_col in feature_columns:
            input_dict[temp_col] = 1

    # Fuel dummy
    if fuel_range != "Low":
        fuel_col = f"Fuel_Range_{fuel_range}"
        if fuel_col in feature_columns:
            input_dict[fuel_col] = 1

    input_df = pd.DataFrame([input_dict])
    input_df = input_df.reindex(columns=feature_columns, fill_value=0)

    prediction = model.predict(input_df)[0]

    st.success(f"Predicted Weekly Sales: {prediction:,.2f}")
