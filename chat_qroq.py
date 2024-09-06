import streamlit as st
import os
import json
from groq import Groq

# Securely load API key
api_key = "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"

client = Groq(api_key=api_key)

st.title("Chat Bot by NS")

# Load chat history from JSON file (if exists)
if os.path.exists("chat_history.json"):
    with open("chat_history.json", "r") as f:
        st.session_state.messages = json.load(f)
else:
    st.session_state.messages = []

if "conversation" not in st.session_state:
    st.session_state.conversation = []

# Display existing messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Handle user input
user_input = st.chat_input("Type something")

if user_input:
    # Append user message to conversation and display it
    user_message = {"role": "user", "content": user_input}
    st.session_state.conversation.append(user_message)
    st.session_state.messages.append(user_message)

    with st.chat_message("user"):
        st.markdown(user_input)

    try:
        # Get chat completion from the API
        chat_completion = client.chat.completions.create(
            messages=st.session_state.conversation,
            model="llama3-70b-8192",
        )

        if chat_completion.choices:
            assistant_message = chat_completion.choices[0].message.content
            assistant_response = {"role": "assistant", "content": assistant_message}

            # Append assistant message to conversation and display it
            st.session_state.conversation.append(assistant_response)
            st.session_state.messages.append(assistant_response)

            with st.chat_message("assistant"):
                st.markdown(assistant_message)
        else:
            st.warning("Assistant did not provide a response.")
    except Exception as e:
        st.error(f"An error occurred: {e}")

    # Save chat history to JSON file
    with open("chat_history.json", "w") as f:
        json.dump(st.session_state.messages, f)