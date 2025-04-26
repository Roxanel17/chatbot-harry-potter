from openai import OpenAI
import streamlit as st
# from dotenv import load_dotenv
import os
import faiss
import numpy as np

client = OpenAI(
  api_key = st.secrets["OPENAI_API_KEY"]
)

st.set_page_config(page_title = "Harry Potter Chatbot", page_icon = ":sparkles:", layout = "wide")
# st.title("Harry Potter Chatbot")
st.title("✨🧙🏻Harry Potter Chatbot✨🧙🏻")

# Search knowledge using embeddings --> instead of feeding allt ext at once, you search smartly and only send relevant parts
# create text chunks
# def split_text(text, chunk_size=500):
#     return [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]

# # create embeddings and build a search index
# def get_embeddings(text):
#     result = client.embeddings.create(
#         model="text-embedding-ada-002",
#         input=text
#     )
#     return result['data'][0]['embedding']

# chunks = split_text(st.sess)

# Initialize session state to store chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are an expert about Harry Potter. Only answer questions related to Harry Potter."}
    ]

# Display previous chat messages
for msg in st.session_state.messages[1:]:  # Skip system message (the initial system prompt)
    if msg["role"] == "user":
        with st.chat_message("user"):
            st.markdown(msg["content"])
    else:
        with st.chat_message("assistant"):
            st.markdown(msg["content"])

# User Input at the bottom
if prompt := st.chat_input("Ask me anything about Harry Potter..."):
    # Add user message to the chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Add a precheck message for nonrelated user inputs:

    keywords = ["harry", "hogwards", "dumbledore", "ron", "hermione", "voldemort", "snape", "sirius", "luna", "hagrid", "granger", "weasley", "wizard", "magic"
                , "quidditch", "wand", "spell", "potion", "house", "gryffindor", "slytherin", "ravenclaw", "hufflepuff", "diagon alley", "muggle", "goblin", "elf", "broomstick"]
    
    if not any(keyword.lower() in prompt.lower() for keyword in keywords):
        # If no keyword found, respond with a message
        assistant_message = " ⚡️ Sorry, I can only answer questions related to Harry Potter."
        
        # Add assistant response
        st.session_state.messages.append({"role": "assistant", "content": assistant_message})
        
        # Show message
        with st.chat_message("user"):
            st.markdown(prompt)
        with st.chat_message("assistant"):
            st.markdown(assistant_message)
    else:
        # Get assistant response (from OpenAI)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=st.session_state.messages
        )

        #Extract the assistant's reply
        # assistant_message = response['choices'][0]['message']['content']
        assistant_message = response.choices[0].message.content

        # Add assistant response to the chat hostory
        st.session_state.messages.append({"role": "assistant", "content": assistant_message})

        # Show latest messages
        with st.chat_message("user"):
            st.markdown(prompt)
        with st.chat_message("assistant"):
            st.markdown(assistant_message)