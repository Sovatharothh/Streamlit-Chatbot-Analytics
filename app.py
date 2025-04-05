import time
import os
import streamlit as st
import pandas as pd
from dotenv import load_dotenv
from pandasai import SmartDataframe
from google_gemini import GoogleGemini  
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')

# Load environment variables
load_dotenv()

# Configure Gemini
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    st.error("Please set GEMINI_API_KEY in your .env file")
    st.stop()

# Initialize Gemini LLM with working model name
llm = GoogleGemini(
    api_key=GEMINI_API_KEY,
    model="models/gemini-1.5-pro-001",
)

# Streamlit web app configuration
st.title("AUPPSearch")

# Initialize session state
if "conversation" not in st.session_state:
    st.session_state.conversation = []
if "plots" not in st.session_state:
    st.session_state.plots = {}

# File uploader
uploaded_file = st.file_uploader("Upload a file (CSV, Excel, or JSON)")

# File processing
if uploaded_file:
    try:
        start_time = time.time()
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        elif uploaded_file.name.endswith('.xlsx'):
            df = pd.read_excel(uploaded_file, engine="openpyxl")
        elif uploaded_file.name.endswith('.json'):
            df = pd.read_json(uploaded_file)
        else:
            st.error("Unsupported file type.")
            df = None

        if df is not None:
            st.write("Dataset Preview:", df.head(6))
            sdf = SmartDataframe(df, config={
                "llm": llm,
                "enable_cache": False
            })
            st.success("File loaded successfully.")
        st.write(f"File loading time: {time.time() - start_time:.2f} seconds")
    except Exception as e:
        st.error(f"Error reading file: {e}")

# Display chat history
for i, message in enumerate(st.session_state.conversation):
    role = message["role"]
    content = message["content"]

    if role == "user":
        with st.chat_message("user"):
            st.markdown(content)
    elif role == "assistant":
        with st.chat_message("assistant"):
            st.markdown(content)
            if i in st.session_state.plots:
                st.pyplot(fig=st.session_state.plots[i])

# Chat input
prompt = st.chat_input("Enter your prompt")

if prompt:
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.conversation.append({"role": "user", "content": prompt})

    with st.spinner("Generating response..."):
        try:
            response = sdf.chat(prompt)
            st.session_state.conversation.append({"role": "assistant", "content": response})

            with st.chat_message("assistant"):
                st.markdown(response)
                if plt.get_fignums():
                    fig_to_store = plt.gcf()
                    st.session_state.plots[len(st.session_state.conversation) - 1] = fig_to_store
                    st.pyplot(fig=fig_to_store)

        except Exception as e:
            error_message = f"Error: {str(e)}"
            st.session_state.conversation.append({"role": "assistant", "content": error_message})
            st.error(error_message)
