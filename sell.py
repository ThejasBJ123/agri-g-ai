import streamlit as st
from google import genai

# Configure Gemini AI Client
client = genai.Client(api_key="AIzaSyAaauGukkzhH0kYGRoFvpOSVY_CdsYiwD0")

# Set Page Config
st.set_page_config(page_title="Smart Crop Price Advisor", layout="wide")

# Custom Styling to Match Website Theme
st.markdown(
    """
    <style>
        body {
            background-color: #ECF8EC;
        }
        .stApp {
            background-color: #ECF8EC;
            color: #1A3C1A;
        }
        .stButton > button {
            background-color: #00A650;
            color: white;
            border-radius: 10px;
            font-size: 18px;
            padding: 10px;
            width: 100%;
        }
        .stTextInput > div > div > input {
            background-color: #F8FFF8;
            border-radius: 10px;
            padding: 10px;
        }
        .stSelectbox > div > div > div > div {
            background-color: #F8FFF8;
            border-radius: 10px;
            padding: 10px;
            height: 50px;        }
        .title-text {
            font-size: 34px;
            font-weight: bold;
            color: #1A3C1A;
            text-align: center;
        }
        .info-text {
            font-size: 16px;
            text-align: center;
            color: #4C7C4C;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Title
st.markdown("<div class='title-text'>🌱 Smart Crop Price Advisor at Agriculture-G-AI</div>", unsafe_allow_html=True)

# Subtitle
st.markdown("<p class='info-text'>Analyze crop prices & discover the best time to sell for maximum profit.</p>", unsafe_allow_html=True)

# Input Fields
col1, col2 = st.columns(2)
with col1:
    crop = st.selectbox("Select Crop", ["Wheat", "Rice", "Maize", "Soybean", "Cotton", "Sugarcane", "Pulses"])
with col2:
    location = st.text_input("Enter Location (City/District/State)")

# Prediction Function
def predict_crop_prices(crop, location):
    prompt = f"""
    Analyze the price trends of {crop} in {location}. Compare:
    - Government MSP (Minimum Support Price)
    - Market Prices (Wholesale & Retail)
    - Private Buyer Prices
    
    Provide a comparative table and predict how the price will change over the next 6 months.
    Suggest the best time to sell for maximum profit based on seasonal trends. Try to be a bit brief and concise. If possible give link of goverment website for MSP.
    Try to give the actual data in the table and don't write that this is example data.
    
    End with: "Thank you for using the Smart Crop Price Advisor at Agriculture-G-AI 🌱🌱🌱🌱."
    """
    response = client.models.generate_content(model="gemini-2.0-flash", contents=prompt)
    return response.text if response and hasattr(response, 'text') else "Could not fetch price trends."

# Button & Output
if st.button("📊 Analyze Prices & Recommend Best Selling Time"):
    if location:
        price_analysis = predict_crop_prices(crop, location)
        st.success(price_analysis)
    else:
        st.warning("Please enter a location for accurate price prediction.")
