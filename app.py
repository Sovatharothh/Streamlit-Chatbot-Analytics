import time
import os
import openai
import streamlit as st
import pandas as pd
from dotenv import load_dotenv
from pandasai import SmartDataframe
from pandasai.llm import GoogleGemini
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
llm = GoogleGemini(api_key=openai.api_key)

# Streamlit web app configuration
st.title("AUPPSearch")

# Initialize conversation history in session state
if "conversation" not in st.session_state:
    st.session_state.conversation = []

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

        # Display preview data
        if df is not None:
            st.write("Dataset Preview:", df.head(6))
            sdf = SmartDataframe(df, config={"llm": llm})
            st.success("File loaded successfully.")
        st.write(f"File loading time: {time.time() - start_time:.2f} seconds")
    except Exception as e:
        st.error(f"Error reading file: {e}")

# Display the chat history
for message in st.session_state.conversation:
    if message["role"] == "user":
        with st.chat_message("user"):
            st.markdown(message["content"])
    elif message["role"] == "assistant":
        with st.chat_message("assistant"):
            st.markdown(message["content"])

# Chat input for user prompt
prompt = st.chat_input("Enter your prompt")

# Handle user input and assistant response
if prompt:
    # Display user's input message
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.conversation.append({"role": "user", "content": prompt})

    # Generate and display assistant's response
    with st.spinner("Generating response..."):
        try:
            # Get response from SmartDataframe
            response = sdf.chat(prompt)

            # Save assistant response to session state
            st.session_state.conversation.append({"role": "assistant", "content": response})

            # Display assistant's message
            with st.chat_message("assistant"):
                st.markdown(response)

            # Check if a figure was generated before displaying it
            if plt.get_fignums(): 
                fig_to_plot = plt.gcf()
                st.pyplot(fig=fig_to_plot)
                # plt.clf()  
        except Exception as e:
            error_message = f"Error: {e}"
            st.session_state.conversation.append({"role": "assistant", "content": error_message})
            st.error(error_message)
