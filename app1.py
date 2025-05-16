import streamlit as st
import tensorflow as tf
import numpy as np
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input, decode_predictions
from PIL import Image
from google import genai

# Initialize the Google GenAI client
client = genai.Client(api_key="AIzaSyBfpSy8Z58lhAN2nZI8aV8fwS01RRb_N78")

# Load pre-trained MobileNetV2 model
vision_model = MobileNetV2(weights="imagenet")

def predict_crop_health(img):
    img = img.convert("RGB")
    img = img.resize((224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = preprocess_input(img_array)

    predictions = vision_model.predict(img_array)
    decoded_predictions = decode_predictions(predictions, top=3)[0]

    result = "🌱 **Crop Health Analysis:**\n"
    for i, (_, label, score) in enumerate(decoded_predictions):
        result += f"🔹 {label}: {score * 100:.2f}%\n"
    return result

class AIAgent:
    def __init__(self):
        self.client = client

    def analyze_soil(self, temp, humidity, moisture, soil_type, crop_type, nitrogen, potassium, phosphorus):
        prompt = (
            f"Soil Report:\n"
            f"Temperature: {temp}°C\n"
            f"Humidity: {humidity}%\n"
            f"Moisture: {moisture}%\n"
            f"Soil Type: {soil_type}\n"
            f"Crop Type: {crop_type}\n"
            f"Nitrogen: {nitrogen} mg/kg\n"
            f"Potassium: {potassium} mg/kg\n"
            f"Phosphorous: {phosphorus} mg/kg\n"
            "\nProvide a structured response with clear values for:\n"
            "- **Analysis** (Water required and recommended fertilizer with NPK ratio and amount)\n"
            "- **Key Measures** for soil and crop health (concise and actionable).\n"
            "Ensure responses are in bullet points and numerical format where applicable."
        )

        response = self.client.models.generate_content(model="gemini-2.0-flash", contents=prompt)
        response_text = response.text.strip()

        return response_text

# Instantiate AI Agent
aio_agent = AIAgent()

# Streamlit UI
st.set_page_config(page_title="🌾 AI-Powered Smart Farming Assistant", layout="wide")
st.title("🌾 AI-Powered Smart Farming Assistant")

# Tabs for Soil Analysis and Crop Health Assessment
tabs = ["Soil Analysis", "Crop Health Assessment"]
selected_tab = st.sidebar.radio("Select Analysis", tabs)

if selected_tab == "Soil Analysis":
    st.header("📊 Soil Analysis")
    
    temp = st.slider("Temperature (°C)", 0, 50, 25)
    humidity = st.slider("Humidity (%)", 0, 100, 50)
    moisture = st.slider("Moisture (%)", 0, 100, 30)
    soil_type = st.selectbox("Soil Type", ["Sandy", "Clay", "Loamy", "Silty", "Peaty", "Chalky"])
    crop_type = st.text_input("Crop Type", "Wheat")
    nitrogen = st.slider("Nitrogen (mg/kg)", 0, 200, 50)
    potassium = st.slider("Potassium (mg/kg)", 0, 200, 50)
    phosphorus = st.slider("Phosphorous (mg/kg)", 0, 200, 50)
    
    if st.button("Analyze Soil"):
        response = aio_agent.analyze_soil(temp, humidity, moisture, soil_type, crop_type, nitrogen, potassium, phosphorus)
        st.markdown(response)

elif selected_tab == "Crop Health Assessment":
    st.header("📷 Crop Health Assessment")
    uploaded_file = st.file_uploader("Upload Crop Image", type=["jpg", "png", "jpeg"])
    
    if uploaded_file is not None:
        img = Image.open(uploaded_file)
        st.image(img, caption="Uploaded Image", use_column_width=True)
        result = predict_crop_health(img)
        st.markdown(result)

st.sidebar.markdown("Developed with ❤️ for Smart Farming")
