import streamlit as st
import google.generativeai as genai
from PIL import Image
import io

# Set the title and header of the Streamlit app
st.title("Intelligent Image Interpreter")
st.header("Upload an image and ask a question")

# --- SECURE API KEY RETRIEVAL ---
try:
    # 1. Get the API key securely from the st.secrets object.
    # This reads from your local .streamlit/secrets.toml file.
    api_key = st.secrets["GOOGLE_API_KEY"]

    # 2. Configure the Gemini API
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.5-flash')

    # --- UI and Logic ---

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

# --- ERROR HANDLING FOR MISSING SECRETS ---
except KeyError:
    # This error will occur if GOOGLE_API_KEY is missing from secrets.toml
    st.error("Configuration Error: The GOOGLE_API_KEY secret was not found.")
    st.info("Please ensure your `.streamlit/secrets.toml` file exists and contains `GOOGLE_API_KEY = \"YOUR_KEY\"`")
except Exception as e:
    st.error(f"An unexpected configuration error occurred: {e}")

