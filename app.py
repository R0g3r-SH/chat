import streamlit as st
from streamlit_chat import message
from streamlit.components.v1 import html
from datetime import datetime
import requests

def on_input_change():
    user_input = st.session_state.user_input
    timestamp = datetime.now()
    st.session_state.messages.append({"content": user_input, "sender": "user", "timestamp": timestamp})

    bot_response = get_bot_response(user_input)
    timestamp = datetime.now()
    st.session_state.messages.append({"content": bot_response, "sender": "bot", "timestamp": timestamp})

def get_bot_response(user_input):
    endpoint = "https://fa87-131-178-102-156.ngrok-free.app"
    response = requests.post(endpoint, json={"question": user_input})
    if response.status_code == 200:
        return response.json().get("answer", "Sorry, I couldn't get a response from the bot.")
    else:
        return "Sorry, something went wrong with the bot."

def on_btn_click():
    st.session_state.messages.clear()

st.session_state.setdefault(
    'messages',
    []
)

st.title("Chat placeholder")

chat_placeholder = st.empty()

with chat_placeholder.container():
 
    sorted_messages = sorted(st.session_state['messages'], key=lambda x: x['timestamp'])

    for i, msg in enumerate(sorted_messages):
        if msg['sender'] == 'user':
            message(msg['content'], is_user=True, key=f"{i}_user")
        else:
            message(msg['content'], key=f"{i}", allow_html=True)

    st.button("Clear message", on_click=on_btn_click)

with st.container():
    st.text_input("User Input:", on_change=on_input_change, key="user_input")
