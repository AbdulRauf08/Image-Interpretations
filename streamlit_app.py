import streamlit as st
import google.generativeai as genai
from PIL import Image
import os
import io

# Set the title and header of the Streamlit app
st.title("Intelligent Image Interpreter")
st.header("Upload an image and ask a question")

# Get the API key from environment variables or Streamlit secrets
api_key = os.environ.get("GOOGLE_API_KEY")

if api_key is None:
    st.error("API key not found. Please set the GOOGLE_API_KEY environment variable.")
else:
    genai.configure(api_key=api_key)
    
    # Initialize the Gemini model
    model = genai.GenerativeModel('gemini-1.5-flash')

    # Create the file uploader and text input for the UI
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
    prompt_text = st.text_area("Your Prompt:", "Describe this image in detail.")

    # Check if a file has been uploaded
    if uploaded_file is not None:
        # Display the uploaded image
        st.image(uploaded_file, caption='Uploaded Image.', use_column_width=True)
        
        # Create the 'Interpret Image' button
        if st.button("Interpret Image"):
            if prompt_text:
                with st.spinner('Interpreting image...'):
                    try:
                        # Read the image data and call the Gemini API
                        img = Image.open(uploaded_file)
                        response = model.generate_content([prompt_text, img])
                        
                        # Display the response
                        st.success("Interpretation successful!")
                        st.markdown(f"**API Response:**\n\n{response.text}")
                        
                    except Exception as e:
                        st.error(f"An error occurred: {e}")
            else:
                st.warning("Please enter a prompt.")