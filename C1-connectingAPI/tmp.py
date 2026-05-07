from google import genai
import streamlit as st
import os
from dotenv import load_dotenv
load_dotenv()

client = genai.Client()


st.title("Gemini AI Chat App")

user_input = st.text_input("Ask something")

if st.button("Generate"):
    if user_input:
        with st.spinner("Thinking...."):
            try:
                response = client.models.generate_content(
                    model = "gemini-2.5-flash-lite",
                    contents = user_input
                )
                st.success("Response: ")
                st.write(response.text)
            except Exception as e:
                st.error(f'Error: {e}')


# python3 C1-connectingAPI/tmp.py

# streamlit run C1-connectingAPI/tmp.py