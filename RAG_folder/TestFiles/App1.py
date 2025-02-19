import streamlit as st
import requests

# Streamlit Page Config
st.set_page_config(page_title="💬 LLaMA Chatbot", layout="wide")

st.title("🤖 LLaMA Chatbot")

# Ready-made questions
ready_questions = ["What is AI?", "How does LLaMA work?", "Tell me a joke"]

# Session State for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message("🤖" if msg["role"] == "bot" else "👤"):
        st.markdown(msg["content"])

# Function to send message to .NET API
def send_message_to_api(user_message):
    api_url = "https://localhost:44355/Forms/Ai.aspx/GetData"   
    response = requests.post(api_url, json={"message": user_message})
    return response.json().get("response", "No response from API.")

# User input field
if user_input := st.chat_input("Type your message..."):
    st.session_state.messages.append({"role": "user", "content": f"👤 {user_input}"})
    
    # Call .NET API for response
    bot_response = send_message_to_api(user_input)
    st.session_state.messages.append({"role": "bot", "content": f"🤖 {bot_response}"})

# Ready-made questions
st.markdown("### Quick Questions:")
col1, col2, col3 = st.columns(3)
if col1.button(ready_questions[0]):
    user_input = ready_questions[0]
if col2.button(ready_questions[1]):
    user_input = ready_questions[1]
if col3.button(ready_questions[2]):
    user_input = ready_questions[2]

# Clear chat button
if st.button("🗑️ Clear Chat"):
    st.session_state.messages = []
    st.experimental_rerun()
