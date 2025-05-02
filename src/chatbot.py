from openai import OpenAI
import streamlit as st
import os
import faiss
import numpy as np
from constants import CHARACTER_LIST, HARRY_POTTER_KEYWORDS, CHARACTER_AVATARS, CHARACTER_HOUSE, HOUSE_COLORS
from helpers import get_character_prompt, get_character_greeting
import time


# --- 1. Setup ---

client = OpenAI(
  api_key = st.secrets["OPENAI_API_KEY"]
)

st.set_page_config(page_title = "Harry Potter Chatbot", page_icon = ":sparkles:", layout = "wide")
st.title("✨🧙🏻Harry Potter Chatbot✨🧙🏻")

# --- 2. Session State ---

# Session flag bot_just_replied
if "bot_just_replied" not in st.session_state:
    st.session_state.bot_just_replied = False

# Initialize character chat histories ---->
# -- Instead of ONE messages history => create ONE per character => each character has their own chat memory =>  switch between Dumbledore and Snape, and each one keeps their own memory
if "character_chats" not in st.session_state:
    st.session_state.character_chats = {}

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

# Update preference
st.session_state.preffered_character = character

# Show specific character greeting
st.markdown(
    f"<p style='text-align: center; font-size: 18px; margin-top: -10px; color: #cccccc;'>{get_character_greeting(character)}</p>",
    unsafe_allow_html=True
)

# --- 3. House + Styling ---

# Get the house color
house = CHARACTER_HOUSE.get(character, "None")
bubble_color = HOUSE_COLORS.get(house, "#aaaaaa")
avatar_url = CHARACTER_AVATARS.get(character)

# --- 4. Initialize or Reset Character Chat ---

# Character has a chat history. If character not in memory yet, create system prompt
if character not in st.session_state.character_chats:
    st.session_state.character_chats[character] = [
        {"role": "system", "content": get_character_prompt(character)}
    ]

# Use selected character's chat history 
chat_history = st.session_state.character_chats[character]

# Add a button to start new chat
if st.button("🔄 Start New Chat"):
    st.session_state.character_chats[character] = [
        {"role": "system", "content": get_character_prompt(character)}
    ]
    chat_history = st.session_state.character_chats[character]

# Initialiaze last character if it doesn't exist
if "last_character" not in st.session_state:
    st.session_state.last_character = character

# --- 5. Display Chat History ---

# Display previous chat messages
for msg in chat_history[1:]:  # Skip system message (the initial system prompt)
    if msg["role"] == "user":
        with st.chat_message("user"):
            st.markdown(msg["content"])
    else:
        with st.chat_message("assistant", avatar = avatar_url):
            st.markdown(
                f"""
                <div style="background-color: {bubble_color}; padding: 10px; border-radius: 10px; color: white;">
                    {msg['content']}
                </div>
                """,
                unsafe_allow_html=True
            )

# --- 6. User Input ---

# User Input at the bottom
if prompt := st.chat_input("Ask me anything about Harry Potter..."):
    
     # Show message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Add user message to the chat history
    chat_history.append({"role": "user", "content": prompt})

    # Add a LLM-base precheck because sometimes using keywords-based checking classifies a related question as non-related
    # --- LLM precheck to detect Harry Potter context ---
    precheck = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system", 
                # Few-Shot prompting:
                "content": (
                    "You're a classifier assistant. Your task is to determine if a user's question is related to the world of Harry Potter.\n\n"
                    "A questions is related if it:\n"
                    "- References a character, creature, house-elf, spell, place, object, magical concept, or event from Harry Potter\n"
                    "- Involves specific behaviors, memories, or traits of known chracters (e.g. 'Do you like socks?' is related to Dobby)\n"
                    "- Mentions Hogwarts, Diagon Alley, Quidditch, or any other Harry Potter-related term\n"
                    "- Is vague but being asked to a Harry Potter character (like 'Who was kind to you?')\n\n"
                    "Examples:\n"
                    "Q: Do you like socks? → Yes\n>"
                    "Q: What's your favorite food? → Yes\n>"
                    "Q: How do you feel about Dumbledore? → Yes\n>"
                    "Q: What is 2 + 2? → No\n>"
                    "Q: Tell me a jock about cats. → No\n\n>"
                    "Respond only with 'Yes' or 'No'.\n"
                    "If you are unsure, respond with 'No'.\n"
                )
                
            },
            {"role": "user", "content": prompt}
        ]
    )
    is_related = precheck.choices[0].message.content.strip().lower()

    if is_related.startswith("no"):
        # If no keyword found, respond with a message
        assistant_message = " ⚡️ Sorry, I can only answer questions related to Harry Potter."
        
        # Add assistant response
        chat_history.append({"role": "assistant", "content": assistant_message})
        
        # Set the flag for bot just replied
        st.session_state.bot_just_replied = True

        
        # Typing animations for replies
        with st.chat_message("assistant", avatar = avatar_url):
            typing_placeholder = st.empty()

            # Typing animation for reply
            typing_placeholder.markdown("🪄 Thinking<span style='font-size:24px'>...</span> ✨", unsafe_allow_html=True) 
            time.sleep(0.2)
            typing_placeholder.markdown(
                f""" 
                <div style = "background-color: {bubble_color}; padding: 10px; border-radius: 10px; color: white;">
                    {assistant_message}
                </div>
                """,
                unsafe_allow_html = True
            )
    else:
        # Typing animations for replies
        with st.chat_message("assistant", avatar = avatar_url):
            typing_placeholder = st.empty()
            
            # Realistic typing dots animation for reply
            for _ in range(2):  # loop cycles
                for dots in [".", "..", "..."]:
                    typing_placeholder.markdown(f"🪄 **Thinking{dots}** ✨", unsafe_allow_html=True)
                    # Add a delay to simulate typing
                    time.sleep(0.2)

        # Get assistant response (from OpenAI)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=chat_history
        )

        #Extract the assistant's reply
        assistant_message = response.choices[0].message.content

        # Add assistant response to the chat hostory
        chat_history.append({"role": "assistant", "content": assistant_message})

        # Update bot just replied flag
        st.session_state.bot_just_replied = True

        # Replace placeholder with the real chatbot response:
        typing_placeholder.markdown(
            f""" 
            <div style = "background-color: {bubble_color}; padding: 10px; border-radius: 10px; color: white;">
                {assistant_message}
            </div>
            """,
            unsafe_allow_html = True
        )