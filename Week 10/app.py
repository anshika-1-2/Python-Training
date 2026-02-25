import streamlit as st
import tensorflow as tf
import numpy as np
from PIL import Image

st.set_page_config(
    page_title="Apple Detection Systemm",
    layout="centered"
)

@st.cache_resource
def load_model():
    """
    Load the apple detection model from disk.

    Returns
    -------
    tf.keras.Model
        The loaded apple detection model.
    """
    return tf.keras.models.load_model("apple_binary_model.h5")

model = load_model()

IMG_SIZE = (128, 128)

# Custom Styling

st.markdown("""
    <style>
    .main {
        background-color: #0E1117;
    }
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        height: 3em;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.title("Apple Detection System")
st.write("Upload an image to classify it as Apple or Not Apple.")

st.divider()

# File Upload
uploaded_file = st.file_uploader(
    "Upload Image",
    type=["jpg", "jpeg", "png"]
)

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGB")

    col1, col2 = st.columns(2)

    with col1:
        st.image(image, caption="Uploaded Image", width="stretch")
    with col2:
        # Preprocess
        img = image.resize(IMG_SIZE)
        img_array = np.array(img)
        img_array = np.expand_dims(img_array, axis=0)

        # Prediction
        prediction = model.predict(img_array)[0][0]

        apple_prob = 1 - prediction
        non_apple_prob = prediction

        st.subheader("Prediction Result")

        if prediction < 0.5:
            st.success("APPLEEEEEEEEEE!!!!!!!!!")
            st.progress(int(apple_prob * 100))
            st.write(f"Confidence: **{apple_prob*100:.2f}%**")
        else:
            st.error("NOT an Apple")
            st.progress(int(non_apple_prob * 100))
            st.write(f"Confidence: **{non_apple_prob*100:.2f}%**")

        st.write(" Probability Breakdown")
        st.write(f"Apple: {apple_prob*100:.2f}%")
        st.write(f"Non-Apple: {non_apple_prob*100:.2f}%")
        
        
st.divider()
st.caption("Model: Binary Classification")