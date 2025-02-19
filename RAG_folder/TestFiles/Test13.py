import streamlit as st
import requests
import ollama

# Set white theme
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

# Chat History
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Function to call Llama API
def call_llama_api(user_message):
    response = ollama.chat(model="llama3", messages=[{"role": "user", "content": user_message}])
    return response.get("message", {}).get("content", "Error: No response received")

# User Input and Search System Checkbox
col1, col2 = st.columns([4, 1])

with col1:
    user_input = st.chat_input("Message")

with col2:
    search_system_data = st.checkbox("Search system data", value=False, label_visibility="hidden")

if user_input:
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    
    with st.spinner("🤖 Thinking..."):
        bot_response = call_llama_api(user_input)
    
    st.session_state.chat_history.append({"role": "assistant", "content": bot_response})
    st.rerun()

# Buttons for predefined queries
cols = st.columns(2)
button_clicked = None

if cols[0].button("Summary"):
    button_clicked = "Summary"
if cols[1].button("Progress"):
    button_clicked = "Progress"

if button_clicked:
    st.session_state.chat_history.append({"role": "user", "content": button_clicked})
    
    with st.spinner("🤖 Thinking..."):
        bot_response = call_llama_api(button_clicked)
    
    st.session_state.chat_history.append({"role": "assistant", "content": bot_response})
    st.rerun()

# Display Chat History
for chat in st.session_state.chat_history:
    if chat["role"] == "user":
        st.chat_message("user").write(chat["content"])
    else:
        st.chat_message("assistant").write(chat["content"])
