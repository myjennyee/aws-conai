import streamlit as st
import requests
import json
import ollama
import pandas as pd
from API.WebServices import call_aspx_webmethod, call_llama_api, get_chat_history

# Set white theme
st.set_page_config(page_title="WYT AI", layout="wide", initial_sidebar_state="expanded")

st.markdown(
    """
    <style>
   textarea ::placeholder {
  color: black !important;
   
}
textarea::-webkit-input-placeholder{
    color:grey !important;
}
textarea::-moz-placeholder {
    color:grey !important;
}
        .stApp, textarea {
            background-color: white !important;
            color: black !important;
            border-color:grey;
            min-height:100px;
             caret-color: black !important;
        }
        .stChatMessage {
            background-color: #f8f9fa !important;
            color: black !important;
            border-radius: 10px;
            padding: 10px;
        }
.stAppHeader,header.stAppHeader ,.st-emotion-cache-h4xjwg
{
backgroundcolor:white !important;
display:none;color:red !important; 
} 
div.stStatusWidget
{ 
color:red !important;
}
header.stAppHeader> label, header.stAppHeader > img,header.stAppHeader > span
{ 
}

        div.stChatMessageContent, .stChatMessageContent, .stMarkdownContainer, 
        div.stMarkdownContainer > p, div.stMarkdown, div.stMarkdown> div> p {  
            color: black !important;
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

        /* Custom styling for input text box */
        textarea.st-ae {
            background-color: white !important;
            color: black !important;
            
        }

        /* Placeholder text color */
        textarea.st-ae input::placeholder {
            color: black !important;   
            font-style: italic;   
        }

        /* Change hover color of placeholder text */
        textarea.st-ae:hover input::placeholder {
            color: grey !important;
        }

        /* Hover effect for the input box */
        textarea.st-ae:hover {
            border-color: #aaa !important;
            box-shadow: 0 0 5px rgba(0, 0, 0, 0.1) !important;
        }
    </style>
    """,
    unsafe_allow_html=True,
)



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

# User Input and Search System Checkbox
col1, col2 = st.columns([4, 1])

with col1:
    user_input = st.chat_input("Message",)

with col2:
    search_system_data =   st.checkbox("Search system data", value=False )

if user_input:
    st.session_state.chat_history.append({"role": "user", "content": user_input})

    # Determine response source
    if search_system_data:
        bot_response = call_llama_api(user_input)
    else:
        response = ollama.chat(model="llama3", messages=[{"role": "user", "content": user_input}])
        bot_response = response.get("message", {}).get("content", "Error: No response received")

    st.session_state.chat_history.append({"role": "assistant", "content": bot_response})

    # If system data search is enabled, call the WebMethod API
    bot_response_result = "No additional data fetched."
    if search_system_data:
        with st.spinner("Fetching system data..."):
            bot_response_result =call_aspx_webmethod(bot_response)
        st.session_state.chat_history.append({"role": "assistant", "content": bot_response_result})

    st.rerun()

# Display Chat History
# for chat in st.session_state.chat_history:
#     if chat["role"] == "user":
#         st.chat_message("user").write(chat["content"])
#     else:
#         st.chat_message("assistant").write(chat["content"])

# Buttons for predefined queries
# cols = st.columns(2)
# if cols[0].button("Summary"):
#     user_input = "Summary"
#     st.session_state.chat_history.append({"role": "user", "content": user_input})
#     bot_response = ollama.chat(model="llama3", messages=[{"role": "user", "content": user_input}]).get("message", {}).get("content", "Error: No response received")
#     st.session_state.chat_history.append({"role": "assistant", "content": bot_response})
#     st.rerun()

# if cols[1].button("Progress"):
#     user_input = "Progress"
#     st.session_state.chat_history.append({"role": "user", "content": user_input})
#     bot_response = ollama.chat(model="llama3", messages=[{"role": "user", "content": user_input}]).get("message", {}).get("content", "Error: No response received")
#     st.session_state.chat_history.append({"role": "assistant", "content": bot_response})
#     st.rerun()

cols = st.columns([1, 1], gap="small")

with cols[0]:
    if st.button("Summary"):
        user_input = "Summary"
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        bot_response = ollama.chat(model="llama3", messages=[{"role": "user", "content": user_input}]).get("message", {}).get("content", "Error: No response received")
        st.session_state.chat_history.append({"role": "assistant", "content": bot_response})
        st.rerun()

with cols[1]:
    if st.button("Progress"):
        user_input = "Progress"
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        bot_response = ollama.chat(model="llama3", messages=[{"role": "user", "content": user_input}]).get("message", {}).get("content", "Error: No response received")
        st.session_state.chat_history.append({"role": "assistant", "content": bot_response})
        st.rerun()