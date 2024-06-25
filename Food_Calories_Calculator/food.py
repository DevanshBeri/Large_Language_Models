from dotenv import load_dotenv
import streamlit as st
import google.generativeai as genai
from PIL import Image

# Load environment variables
load_dotenv()

# Set API key for Google Gemini Pro Vision API
Google_Api = "AIzaSyDzr_W9udJF9Uz0ZjSE7fpXo1AB4FW3bDU"
genai.configure(api_key=Google_Api)

def get_gemini_response(image, prompt):
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([image, prompt])
    return response.text

def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        image_parts = {
            "mime_type": uploaded_file.type,
            "data": bytes_data
        }
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")

# Set Streamlit page configuration
st.set_page_config(page_title="Food Calories Calculator 🤤🤤")

# Initialize chat history in session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Set sidebar for drag-and-drop file uploader
st.sidebar.markdown("<h2 style='text-align: center;'>Drag and Drop Image Here</h2>", unsafe_allow_html=True)
uploaded_file = st.sidebar.file_uploader("", type=["jpg", "jpeg", "png"], accept_multiple_files=False)

# Main content in the center
st.markdown("<h1 style='text-align: center;'>Food Calories Calculator 🤤🤤</h1>", unsafe_allow_html=True)

# Function to display chat history
def display_chat_history():
    if st.session_state.chat_history:
        st.subheader("Chat History:")
        for interaction in st.session_state.chat_history:
            st.write(f"- **{interaction['type'].capitalize()}**: {interaction['message']}")
            st.write(f"  Response: {interaction['response']}")
            st.write("\n\n")
       

           


# Handle uploaded file
if uploaded_file is not None:
    st.markdown(f"**The uploaded image is:** {uploaded_file.name}")
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)
   
    # Button to submit the image
    submit_calories = st.button("Tell me the details about the food item")

    if submit_calories:
        try:
            image_data = input_image_setup(uploaded_file)
            input_prompt = """
            You are an expert in nutritionist where you need to see the food items from the image and tell the following about the food 

            1) Name of the meal or food in the format (The name of food is ......)

            2) Calculate the total calories in the format (The total calories in the food is .....)

            3) (The various food items present in the meal along with calories present are as follows) Also provide the details of every food items with calories intake in below format. Each item in different line

               1. Item 1 - no of calories
               2. Item 2 - no of calories
               ----
               ----

            4) Finally you can also mention whether the food is healthy or not. Also explain the reason behind your decision about healthy or not in detail in 30-40 words

            5) (The Various nutrients component present in food are) Also mention the percentage split of the ratio of carbohydrates, fats, fibre, sugar, and other things required in the diet in the format 

               1) protein % is
               2) carbohydrates % is
               -----
               -----

            Make sure you give the detailed information about each and every point i.e from Name of food to Percentage Split 
            """

            response = get_gemini_response(image_data, input_prompt)
            st.subheader("The Response is")
            st.write(response)
            
            # Add interaction to session chat history
            st.session_state.chat_history.append({"type": "image_upload", "message": f"Uploaded image: {uploaded_file.name}", "response": response})
        except Exception as e:
            st.error(f"An error occurred: {e}")

# Ask question section
user_question = st.text_input("Ask a question about the food in the image:")
submit = st.button("Ask")

if submit and user_question:
    try:
        # Prepare input for the Gemini model
        image_data = input_image_setup(uploaded_file)
        response = get_gemini_response(image_data, user_question)
        st.subheader("Response:")
        st.write(response)
        
        # Add interaction to session chat history
        st.session_state.chat_history.append({"type": "user", "message": user_question, "response": response})
    except Exception as e:
        st.error(f"An error occurred: {e}")

# Display link for chat history
if st.session_state.chat_history:
    if st.sidebar.checkbox("Show Chat History"):
        display_chat_history()
