# Character selection for prompt customization

import json
from pathlib import Path

# Load character prompts from JSON file
CHARACTER_PROMPTS = json.loads(Path("src/character_prompts.json").read_text())

def get_character_prompt(character):
    if character in CHARACTER_PROMPTS:
        entry = CHARACTER_PROMPTS[character]
        base_prompt = entry["prompt"]
        examples = "\n\n".join(
            f"User: {ex['user']}\n{character}: {ex['bot']}" for ex in entry.get("examples", [])
        )
        return f"{base_prompt}\n\nExamples:\n{examples}"
    else:
        return "You are an expert on the world of Harry Potter. Answer only Harry Potter–related questions."

# Customs greetings lines for each character

def get_character_greeting(character):
    greetings = {
        "Albus Dumbledore": "Welcome, young wizard. How may I assist you today?",
        "Severus Snape": "I trust your questions won't waste my time.",
        "Harry Potter": "Hey there! I'm Harry. Want to talk about magic or Hogwarts?",
        "Lord Voldemort": "Speak... if you dare.",
        "Hermione Granger": "Books and cleverness... ask me anything factual. I hope you’ve done your reading. What would you like to learn today?",
        "Hagrid": "Blimey! What can I help yeh with? Hope it's not about dragons!",
        "Dobby": "Dobby is free and happy to help you, kind wizard! What does the master need?",
        "Ron Weasley": "Uh... let's hope I know the answer. Fire away!",
        "Luna Lovegood": "The world is full of wonders, isn't it? The Nargles told me you’d visit. Let’s chat!",
        "Sirius Black": "What mischief shall we discuss today? Ready for some fun?"
    }
    return greetings.get(character, "Greetings, ask away.")