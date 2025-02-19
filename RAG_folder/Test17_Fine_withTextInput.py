import streamlit as st
import requests
import ollama

# Set page config
st.set_page_config(page_title="WYT AI", layout="wide", initial_sidebar_state="expanded")

# WebMethod API URL (hosted on IIS)
WEBMETHOD_URL = "https://localhost:44355/Forms/Ai.aspx/GetChatbotResponse"  # Change this to actual URL

# Function to call ASPX WebMethod API
def call_aspx_webmethod(user_message):
    headers = {"Content-Type": "application/json"}
    payload = {"userMessage": user_message}
    try:
        response = requests.post(WEBMETHOD_URL, json=payload, headers=headers, verify=False)
        return response.text
    except requests.exceptions.RequestException as e:
        return f"Error: {e}"

# Initialize session state variables
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "last_input" not in st.session_state:
    st.session_state.last_input = ""

if "trigger_summarize" not in st.session_state:
    st.session_state.trigger_summarize = False  # Separate flag for summarization

# Display chat history
for chat in st.session_state.chat_history:
    if chat["role"] == "user":
        st.chat_message("user").write(chat["content"])
    else:
        st.chat_message("assistant").write(chat["content"])

# User Input
user_input = st.text_input("Enter your message:", key="user_input_key")  # Unique key

# Button Section (Summary)
col1, col2 = st.columns([1, 1])
with col1:
    if st.button("Summarize"):
        if st.session_state.last_input:
            st.session_state.trigger_summarize = True  # Trigger summarization

# **Process User Input (Avoids duplication)**
if user_input and user_input != st.session_state.last_input:
    st.session_state.last_input = user_input  # Store last input
    print(st.session_state.last_input)
    print(st.session_state.trigger_summarize)
    st.session_state.chat_history.append({"role": "user", "content": user_input})

    # Show loading status
    loading_message = st.empty()
    loading_message.write("🤖 Thinking...")

    # Call Llama 3 API
    response = ollama.chat(model="llama3", messages=[{"role": "user", "content": user_input}])
    bot_response = response.get("message", {}).get("content", "Error: No response received")

    # Clear loading status
    loading_message.empty()

    st.session_state.chat_history.append({"role": "assistant", "content": bot_response})

    st.rerun()

# **Process Summarization (Only Once)**
if st.session_state.trigger_summarize:
    st.session_state.trigger_summarize = False  # Reset trigger

    summary_input = f"Summarize: {st.session_state.last_input}"
    st.session_state.chat_history.append({"role": "user", "content": summary_input})

    # Show loading status
    loading_message = st.empty()
    loading_message.write("🤖 Summarizing...")

    # Call Llama 3 API for summary
    response = ollama.chat(model="llama3", messages=[{"role": "user", "content": summary_input}])
    summary_response = response.get("message", {}).get("content", "Error: No response received")

    # Clear loading status
    loading_message.empty()

    st.session_state.chat_history.append({"role": "assistant", "content": summary_response})

    st.rerun()
