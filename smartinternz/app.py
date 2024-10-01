#Gemini Nutrition APP
from dotenv import load_dotenv
load_dotenv() ## load all the environment variables
import streamlit as st
import os
import google.generativeai as genai 
from PIL import Image
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

input_prompt="""
You are an expert in nutritionist where you need to see the food itens from the image 
            and calculate the total calories, also provide the details of every food items with calorie is below format

            1. Item 1 - no of calories

            2. Item 2 - no of calories
            ----
            ----

"""

def input_image_setup(uploaded_file):
    #Check if a file has been uploaded
    if uploaded_file is not None: # Read the file into bytes
        bytes_data = uploaded_file.getvalue()
        image_parts = [
            {
                "mime_type": uploaded_file.type,
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")
#integrated with webframework
def get_gemini_response(input, image, prompt):
    model=genai.GenerativeModel('gemini-1.5-pro') 
    response=model.generate_content([input, image [0], prompt])
    return response.text

st.set_page_config(page_title="Nutrition App")
st.header("Nutrition App")
input=st.text_input("Input Prompt: ",key="input")
uploaded_file=st.file_uploader("Choose an image ...", type=["jpg", "jpeg", "png"])
image=""
if uploaded_file is not None:
    image=Image.open(uploaded_file)
    st.image(image, caption="uploaded Image.", use_column_width=True)
submit=st.button("Tell me the total calories")
#if submit button is clicked
if submit:
    image_data=input_image_setup(uploaded_file)
    response=get_gemini_response(input, image_data, input_prompt)
    st.subheader=("The Response is")
    st.write(response)
