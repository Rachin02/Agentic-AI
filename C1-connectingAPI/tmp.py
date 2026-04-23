from google import genai
import streamlit as st

client = genai.Client(api_key = "AIzaSyC8M2TgVr3bpoWO1VkVTUDLA2HqevZhF0I")


st.title("Gemini AI Chat App")

user_input = st.text_input("Ask something")

if st.button("Generate"):
    if user_input:
        with st.spinner("Thinking...."):
            try:
                response = client.models.generate_content(
                    model = "gemini-2.5-flash",
                    contents = user_input
                )
                st.success("Response: ")
                st.write(response.text)
            except Exception as e:
                st.error(f'Error: {e}')


# python3 C1-connectingAPI/tmp.py

# streamlit run C1-connectingAPI/tmp.py