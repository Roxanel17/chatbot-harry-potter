from openai import OpenAI
import streamlit as st
# from dotenv import load_dotenv
import os

client = OpenAI(
  api_key = st.secrets["OPENAI_API_KEY"]
)

st.set_page_config(page_title="Harry Potter Chatbot")
st.title("Harry Potter Chatbot")

# Initialize session state to store chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are an expert about Harry Potter. Only answer questions related to Harry Potter."}
    ]
# User Input at the bottom
if prompt := st.chat_input("Ask me anything about Harry Potter..."):
    # Add user message to the chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Get assistant response (from OpenAI)
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=st.session_state.messages
    )

    #Extract the assistant's reply
    assistant_message = response.choices[0].message.content

    # Add assistant response to the chat hostory
    st.session_state.messages.append({"role": "assistant", "content": assistant_message})

# Display previous chat messages
for msg in st.session_state.messages[1:]:  # Skip system message (the initial system prompt)
    if msg["role"] == "user":
        st.write(f"**You:** {msg['content']}")
    else:
        st.write(f"**Chatbot:** {msg['content']}")