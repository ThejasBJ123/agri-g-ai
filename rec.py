import streamlit as st
from google import genai

# Configure Gemini AI Client
client = genai.Client(api_key="AIzaSyBfpSy8Z58lhAN2nZI8aV8fwS01RRb_N78")

# Set Streamlit page config
st.set_page_config(page_title="Agriculture-G-AI - Smart Crop Recommendation", layout="wide")

# Custom styling to match the website
def set_bg_style():
    st.markdown(
        """
        <style>
            body {
                background: linear-gradient(to right, #e6f9e6, #f0fff0);
                color: #2e2e2e;
            }
            .stButton>button {
                background-color: #90EE90;
                color: white;
                font-size: 16px;
                padding: 10px;
                border-radius: 8px;
            }
            .stButton>button:hover {
                background-color: #218838;
            }
            .stTextInput>div>div>input {
                border-radius: 8px;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

set_bg_style()

def recommend_crop_gemini(soil_type, pH, nitrogen, phosphorus, potassium, rainfall, temperature, location):
    """Use Gemini AI to recommend a crop based on input parameters."""
    prompt = f"""
    Based on the following soil and weather conditions, suggest the best crop(s) to grow in {location}:
    - Soil Type: {soil_type}
    - Soil pH: {pH}
    - Nitrogen Level: {nitrogen} ppm
    - Phosphorus Level: {phosphorus} ppm
    - Potassium Level: {potassium} ppm
    - Annual Rainfall: {rainfall} mm
    - Average Temperature: {temperature} °C
    
    Provide region-specific recommendations and explain in brief why the suggested crop is suitable. Don't show much analysis, make the table with a timeline, and write in simple language.
    Start with "Based on the provided conditions, the recommended crop(s) are:"
    End with "Thank you for using the Smart Crop Recommendation System at Agriculture-G-AI 🌾🌾🌾." This should be out of the table.
    """
    
    response = client.models.generate_content(model="gemini-2.0-flash", contents=prompt)
    
    return response.text if response and hasattr(response, 'text') else "Could not fetch recommendation."

# Streamlit UI
st.markdown("""
    <h1 style='color: #2e7d32;'>🌾 Smart Crop Recommendation System at Agriculture-G-AI</h1>
    <p style='font-size:18px;'>Enter your soil and weather details below to get AI-powered crop suggestions.</p>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    soil_type = st.selectbox("🌱 Soil Type", ["Sandy", "Clay", "Loamy", "Silty", "Peaty", "Saline"])
    pH = st.slider("📏 Soil pH", 4.0, 9.0, 6.5)
    nitrogen = st.number_input("🧪 Nitrogen Level (ppm)", 0, 200, 50)
    phosphorus = st.number_input("🧪 Phosphorus Level (ppm)", 0, 200, 50)

with col2:
    potassium = st.number_input("🧪 Potassium Level (ppm)", 0, 200, 50)
    rainfall = st.number_input("🌧️ Annual Rainfall (mm)", 200, 3000, 1200)
    temperature = st.number_input("🌡️ Average Temperature (°C)", 0, 50, 25)
    location = st.text_input("📍 Location (City/District/State)", "")

st.markdown("""
    <p style='color: #888; font-size: 14px;'>Ensure all details are correct for the best recommendations.</p>
""", unsafe_allow_html=True)

# Predict button
if st.button("🚀 Recommend Crop"):
    if location:
        crop_recommendation = recommend_crop_gemini(soil_type, pH, nitrogen, phosphorus, potassium, rainfall, temperature, location)
        st.success(f"🌾 Recommended Crop(s):")
        st.markdown(f"<div style='background: #e9f5e9; padding: 10px; border-radius: 8px; font-size: 16px;'>{crop_recommendation}</div>", unsafe_allow_html=True)
    else:
        st.warning("⚠️ Please enter a location for region-specific recommendations.")
