### Health Management APP
from dotenv import load_dotenv
load_dotenv()  # Load all environment variables

import streamlit as st
import os
import google.generativeai as genai
from PIL import Image

# Configure Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to load Google Gemini Pro Vision API and get response
def get_gemini_response(prompt_text, image, user_input):
    model = genai.GenerativeModel('gemini-2.0-flash')
    response = model.generate_content([prompt_text, image[0], user_input])
    return response.text

# Function to process uploaded image
def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        image_parts = [
            {
                "mime_type": uploaded_file.type,
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        st.error("Please upload an image first")
        return None

# Initialize Streamlit app
st.set_page_config(page_title="Health Management App", layout="centered")
st.title("🍎 Gemini Health App 🍎")  # Mobile-friendly header with emoji

# Input Prompt
user_input = st.text_input("Enter additional info (optional):", key="input")

# Image Uploader
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
image_obj = None
if uploaded_file:
    image_obj = Image.open(uploaded_file)
    st.image(image_obj, caption="Uploaded Image", use_container_width=True)

# Submit Button
submit = st.button("Calculate Total Calories")

# Prompt template
input_prompt = """
You are an expert nutritionist. Analyze the food items in the image
and calculate total calories. Provide details for each item like:

1. Item 1 - calories
2. Item 2 - calories
...
"""

# Run Gemini API when submit is clicked
if submit:
    if uploaded_file:
        image_data = input_image_setup(uploaded_file)
        if image_data:
            with st.spinner("Analyzing image and calculating calories..."):
                response = get_gemini_response(input_prompt, image_data, user_input)
                st.subheader("🍽️ Result")
                st.write(response)
    else:
        st.warning("Please upload an image to get results")
