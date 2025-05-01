from openai import OpenAI
import streamlit as st
import os
import faiss
import numpy as np
from constants import CHARACTER_LIST, HARRY_POTTER_KEYWORDS, CHARACTER_AVATARS, CHARACTER_HOUSE, HOUSE_COLORS
from helpers import get_character_prompt
import time


client = OpenAI(
  api_key = st.secrets["OPENAI_API_KEY"]
)

st.set_page_config(page_title = "Harry Potter Chatbot", page_icon = ":sparkles:", layout = "wide")
st.title("✨🧙🏻Harry Potter Chatbot✨🧙🏻")


# Store and remember user preferences for a character
# Check if character exists
if "preffered_character" not in st.session_state:
    st.session_state.preffered_character = "Harry Potter" # default

# Add character selection box
character = st.selectbox(
     "Select a character:",
     CHARACTER_LIST,
     index = CHARACTER_LIST.index(st.session_state.preffered_character)
 )

# Get the house color
house = CHARACTER_HOUSE.get(character, "None")
bubble_color = HOUSE_COLORS.get(house, "#aaaaaa")

# Update preference
st.session_state.preffered_character = character

# Add a button to start new chat
if st.button("🔄 Start New Chat"):
    st.session_state.messages = [
        {"role": "system", "content": get_character_prompt(character)}
    ]

# Initialiaze last character if it doesn't exist
if "last_character" not in st.session_state:
    st.session_state.last_character = character

# If user changed character, reset chat history
if character != st.session_state.last_character:
    st.session_state.messages = [
        {"role": "system", "content": get_character_prompt(character)}
    ]
    st.session_state.last_character = character

# Initialize session state to store chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": get_character_prompt(character)}
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
    
    if not any(keyword.lower() in prompt.lower() for keyword in HARRY_POTTER_KEYWORDS):
        # If no keyword found, respond with a message
        assistant_message = " ⚡️ Sorry, I can only answer questions related to Harry Potter."
        
        # Add assistant response
        st.session_state.messages.append({"role": "assistant", "content": assistant_message})
        
        # Show message
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Typing animations for replies
        with st.chat_message("assistant", avatar = CHARACTER_AVATARS.get(character)):
            typing_placeholder = st.empty()
            typing_placeholder.markdown("🪄 Thinking<span style='font-size:24px'>...</span> ✨", unsafe_allow_html=True) # Typing animation for reply
            time.sleep(0.2)
            st.markdown(
                f""" 
                <div style = "background-color: {bubble_color}; padding: 10px; border-radius: 10px; color: white;">
                    {assistant_message}
                </div>
                """,
                unsafe_allow_html = True
            )
    else:
        # Show latest messages
        with st.chat_message("user"):
            st.markdown(prompt)

        # Typing animations for replies
        with st.chat_message("assistant", avatar = CHARACTER_AVATARS.get(character)):
            typing_placeholder = st.empty()
            typing_placeholder.markdown("🪄 Thinking<span style='font-size:24px'>...</span> ✨", unsafe_allow_html=True) # Typing animation for reply
        
        # Add a delay to simulate typing
        time.sleep(0.2)

        # Get assistant response (from OpenAI)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=st.session_state.messages
        )

        #Extract the assistant's reply
        assistant_message = response.choices[0].message.content

        # Add assistant response to the chat hostory
        st.session_state.messages.append({"role": "assistant", "content": assistant_message})

        # Replace placeholder with the real chatbot response:
        typing_placeholder.markdown(
            f""" 
            <div style = "background-color: {bubble_color}; padding: 10px; border-radius: 10px; color: white;">
                {assistant_message}
            </div>
            """,
            unsafe_allow_html = True
        )