from openai import OpenAI
import streamlit as st
# from dotenv import load_dotenv
import os

client = OpenAI(
  api_key = st.secrets["OPENAI_API_KEY"]
)

st.set_page_config(page_title="Harry Potter Chatbot")
st.title("Harry Potter Chatbot")

user_input = st.chat_input("Ask me anything about Harry Potter!") 
if user_input:
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an expert about Harry Potter. Only answer questions related to Harry Potter"},
            {"role": "user", "content": user_input}
        ]
    )
    st.write(response.choices[0].message.content)