import streamlit as st
import requests
import ollama

# Set white theme
st.set_page_config(page_title="WYT AI", layout="wide", initial_sidebar_state="expanded")

st.markdown(
    """
    <style>
        .stChatMessage {
            background-color: #f8f9fa !important;
            color: black !important;
            border-radius: 10px;
            padding: 10px;
        }
        .stButton > button {
            background-color: white !important;
            color: black !important;
            border: 2px solid black !important;
            border-radius: 10px !important;
            padding: 8px 16px !important;
            font-size: 14px !important;
            width: 200px;
        }
        .stButton > button:hover {
            background-color: #f0f0f0 !important;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

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

# Display Chat History Above Input Box
chat_container = st.container()

with chat_container:
    for chat in st.session_state.chat_history:
        if chat["role"] == "user":
            st.chat_message("user").write(chat["content"])
        else:
            st.chat_message("assistant").write(chat["content"])

# User Input (always at the bottom)
col1, col2 = st.columns([4, 1])

with col1:
    user_input = st.chat_input("Message")

with col2:
    search_system_data = False

if user_input:
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    
    loading_message = st.empty()
    loading_message.write("🤖 Thinking...")

    if search_system_data:
        bot_response = call_aspx_webmethod(user_input)
    else:
        response = ollama.chat(model="llama3", messages=[{"role": "user", "content": user_input}])
        bot_response = response.get("message", {}).get("content", "Error: No response received")

    loading_message.empty()
    st.session_state.chat_history.append({"role": "assistant", "content": bot_response})
    st.rerun()
