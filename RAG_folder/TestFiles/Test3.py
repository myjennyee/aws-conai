import streamlit as st
import requests
import json
import ollama

# Streamlit UI Setup
st.set_page_config(page_title="WYT AI", layout="wide")
st.title("🤖 WYT AI")

# Your WebMethod URL (hosted on IIS)
WEBMETHOD_URL = "https://localhost:44355/Forms/Ai.aspx/GetChatbotResponse"  # Change this to your actual ASPX URL


# Function to call ASPX WebMethod
def call_aspx_webmethod(user_message):
    headers = {"Content-Type": "application/json"}
    payload = {"userMessage": user_message}  # Use the actual input
    
    try:
        print("📡 Sending request to:", WEBMETHOD_URL)
        print("📨 Payload:", payload)

        response = requests.post(WEBMETHOD_URL, json=payload, headers=headers, verify=False)  # Use json=payload

        print("📩 Raw Response:", response.text)  # Print raw response for debugging

        response.raise_for_status()  # Raise error if HTTP response is not 200

        response_data = response.json()
        print("✅ Parsed Response:", response_data)

        return response_data.get("d", "Error: No response received")  # "d" is the standard ASP.NET wrapper
    except requests.exceptions.RequestException as e:
        print("❌ Error:", e)
        return f"Error: {e}"

# Custom CSS for Messenger-Style Chat UI
st.markdown(
    """
    <style>
        .chat-container {
            display: flex;
            flex-direction: column;
        }
        .chat-bubble {
            padding: 10px 15px;
            border-radius: 20px;
            margin: 5px 0;
            max-width: 75%;
            word-wrap: break-word;
            font-size: 16px;
            display: inline-block;  /* Ensure it wraps around the content */
        }
        .user {
            align-self: flex-end;
            background-color: #0078FF;
            color: white;
            text-align: right;
            float:right;
        }
        .bot {
            align-self: flex-start;
            background-color: #EAEAEA;
            color: black;
            text-align: left;
            float:left;
        }
        
        div.bot > span{
            float:left !important; 
        }
        .stAppHeader
        {
        display:block;
        }
        .highlight {
            background-color: #FFFF99;  /* Highlight color */
        }
        .emoji {
            margin-top: -40px;
            float:right;
            font-size: 20px;
            margin-right: 10px; /* Spacing between emoji and message */
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Ready Question Messages
ready_messages = ["Hello!", "What can you do?", "Tell me a joke", "Goodbye"]

# Chat History
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Function to call Llama (Ollama)
def call_llama_api(user_message):
    response = ollama.chat(model="llama3", messages=[{"role": "user", "content": user_message}])
    return response.get("message", {}).get("content", "Error: No response received")

# Emojis for user and bot
user_emoji = "🙂"  # User emoji
bot_emoji = "🤖"   # Bot emoji

# Chat Display
st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
for chat in st.session_state.chat_history:
    role_class = "user" if chat["role"] == "user" else "bot"
    
    # If user input is "Yes", apply the 'highlight' class
    highlight_class = "highlight" if chat['content'].lower() == "yes" else ""
    
    # Apply emoji based on the role
    emoji = user_emoji if chat["role"] == "user" else bot_emoji
    
    st.markdown(
        f"<div class='chat-bubble {role_class} {highlight_class}'>"
        f"<span class='emoji'>{emoji}</span>{chat['content']}</div>",
        unsafe_allow_html=True,
    )
st.markdown("</div>", unsafe_allow_html=True)

# User Input
user_input = st.chat_input("Type your message...")
if user_input:
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    
    # Get chatbot response
    bot_response = call_llama_api(user_input)
    st.session_state.chat_history.append({"role": "assistant", "content": bot_response})
    
    with st.spinner("Thinking..."):
        bot_response_result = call_aspx_webmethod(user_input)
    # Refresh the chat display
    st.rerun()

# Ready Messages Buttons (Moved to below the input box)
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

# Clear Chat Button
if st.button("🗑️ Clear Chat"):
    st.session_state.chat_history = []
    st.rerun() 
