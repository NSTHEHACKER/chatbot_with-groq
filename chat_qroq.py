import streamlit as st
from groq import Groq

client = Groq(api_key="your_groq_api_key_here"")

conversation = [
    {
        "role": "user",
        "content": "",
    }
]

st.title("Chat Bot by NS")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

userinput = st.chat_input("Type something")

if userinput:
    with st.chat_message("user"):
        st.markdown(userinput)

    st.session_state.messages.append({"role": "user", "content": userinput})
    conversation.append({"role": "user", "content": userinput})

    chat_completion = client.chat.completions.create(
        messages=conversation,
        model="llama3-70b-8192",
    )

    if chat_completion.choices:
        assistant_message = chat_completion.choices[0].message.content

        with st.chat_message("assistant"):
            st.markdown(assistant_message)

        st.session_state.messages.append({"role": "assistant", "content": assistant_message})
    else:
        st.warning("Assistant did not provide a response.")

