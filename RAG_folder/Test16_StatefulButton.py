import streamlit as st
import requests
import json
import ollama

# Set white theme
st.set_page_config(page_title="WYT AI", layout="wide", initial_sidebar_state="expanded")

# Initialize session state variables if not set
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "latest_user_input" not in st.session_state:
    st.session_state.latest_user_input = ""

if "button_clicked" not in st.session_state:
    st.session_state.button_clicked = None  # Track which button was clicked

# User Input
user_input = st.text_input("Message", key="user_input")

if user_input:
    st.session_state.latest_user_input = user_input

# Buttons for actions
cols = st.columns([1, 1], gap="small")

with cols[0]:
    if st.button("Summary"):
        st.session_state.button_clicked = "Summary"

with cols[1]:
    if st.button("Progress"):
        st.session_state.button_clicked = "Progress"

# Check if a button was clicked and process the input
if st.session_state.button_clicked:
    modified_input = f"{st.session_state.button_clicked} {st.session_state.latest_user_input}"

    # Append user input with the button context
    st.session_state.chat_history.append({"role": "user", "content": modified_input})

    # Call Llama API
    response = ollama.chat(model="llama3", messages=[{"role": "user", "content": modified_input}])
    bot_response = response.get("message", {}).get("content", "Error: No response received")

    # Append bot response
    st.session_state.chat_history.append({"role": "assistant", "content": bot_response})

    # Reset button state to avoid repeated execution
    st.session_state.button_clicked = None

    #st.rerun()

# Display Chat History
chat_container = st.container()
with chat_container:
    for chat in st.session_state.chat_history:
        if chat["role"] == "user":
            st.chat_message("user").write(chat["content"])
        else:
            st.chat_message("assistant").write(chat["content"])
