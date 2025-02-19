import streamlit as st
import ollama

# Streamlit UI Setup
st.set_page_config(page_title="Llama Chatbot", layout="wide")
st.title("🤖 Llama Chatbot")

# Ready Question Messages
ready_messages = ["Hello!", "What can you do?", "Tell me a joke", "Goodbye"]

# Chat History
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Function to call Llama (Ollama)
def call_llama_api(user_message):
    response = ollama.chat(model="llama3", messages=[{"role": "user", "content": user_message}])
    return response.get("message", {}).get("content", "Error: No response received")

# Display Chat History
for chat in st.session_state.chat_history:
    with st.chat_message(chat["role"]):
        st.markdown(chat["content"])

# Ready Messages Buttons
st.write("**Quick Messages:**")
cols = st.columns(len(ready_messages))
for i, msg in enumerate(ready_messages):
    if cols[i].button(msg):
        user_input = msg  # Set message from quick reply
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        
        # Get chatbot response
        bot_response = call_llama_api(user_input)
        st.session_state.chat_history.append({"role": "assistant", "content": bot_response})
        
        # Refresh chat immediately
        st.rerun()

# User Input
user_input = st.chat_input("Type your message...")
if user_input:
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    
    # Get chatbot response
    bot_response = call_llama_api(user_input)
    st.session_state.chat_history.append({"role": "assistant", "content": bot_response})
    
    # Refresh the chat display
    st.rerun()

# Clear Chat Button
if st.button("🗑️ Clear Chat"):
    st.session_state.chat_history = []
    st.rerun()
