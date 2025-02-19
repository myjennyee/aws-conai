import streamlit as st
import ollama

# Initialize session state
if "last_input" not in st.session_state:
    st.session_state.last_input = ""

if "button_clicked" not in st.session_state:
    st.session_state.button_clicked = False

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Create a unique key for the input field to reset it after submission
input_key = f"latest_user_input_{st.session_state.button_clicked}"

# User Input
user_input = st.text_input("Message", key=input_key)

# Button Click (Summarize)
if st.button("Summarize"):
    st.session_state.button_clicked = True

# **Process User Input (Avoids duplication)**
if user_input and user_input != st.session_state.last_input:
    st.session_state.last_input = user_input  # Store last input

    # **Check if Enter was Pressed (and NOT the button)**
    if not st.session_state.button_clicked:
        # Handle normal user input (Enter press)
        response = ollama.chat(model="llama3", messages=[{"role": "user", "content": user_input}])
        assistant_response = response.get("message", {}).get("content", "Error: No response")

        # Add to chat history
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        st.session_state.chat_history.append({"role": "assistant", "content": assistant_response})

        # Show the chat history
        for chat in st.session_state.chat_history:
            if chat["role"] == "user":
                st.chat_message("user").write(chat["content"])
            else:
                st.chat_message("assistant").write(chat["content"])

        # **Clear input after processing**
        st.session_state.button_clicked = False

        # Reset the input key to clear the field
        input_key = f"latest_user_input_{st.session_state.button_clicked}"

# **If Button Was Clicked, Process Summarize**
elif st.session_state.button_clicked:
    st.session_state.button_clicked = False  # Reset button state
    response = ollama.chat(model="llama3", messages=[{"role": "user", "content": "Summarize " + user_input}])
    summary_response = response.get("message", {}).get("content", "Error: No response")

    # Add to chat history
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    st.session_state.chat_history.append({"role": "assistant", "content": summary_response})

    # Show the chat history
    for chat in st.session_state.chat_history:
        if chat["role"] == "user":
            st.chat_message("user").write(chat["content"])
        else:
            st.chat_message("assistant").write(chat["content"])

    # **Clear input after processing**
    input_key = f"latest_user_input_{st.session_state.button_clicked}"

