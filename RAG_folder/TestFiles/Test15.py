import streamlit as st
import requests
import json
import ollama
import pandas as pd

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

.stMarkdownContainer, div.stMarkdownContainer p,div.stMarkdownContainer >p{
color:black !important;
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

# Table structure for SQL generation
table_structure = """
Table_Clash: clashId, orgClashTestId, clashName, clashIssue, clashDistance, clashGrid, clashLevel, clashPointX, clashPointY, clashPointZ, item1, item2, image, deleteFlg, description, createdBy, createdDateTime, updatedBy, updatedDateTime
Table_ClashTest: clashTestId, clashTestTimeStamp, orgFile, clashTestZone, clashTestName, tolerance, totalClashes, new, active, reviewed, approved, resolved, type, clashes, deleteFlg, comment, createdBy, createdDateTime, updatedBy, updatedDateTime
Table_Element: elementId, clashId, clashName, orgClashTestId, orgFile, elementItemType, elementCategory, elementFamily, elementType, elementPhase, deleteFlg, comment, createBy, createdDateTime, updatedBy, updatedDateTime
"""

# Function to call Llama for SQL generation
def call_llama_api(user_message):
    message = f"Generate a valid SQL query from the following input: {user_message}. Use the following tables and columns: {table_structure}"
    response = ollama.chat(model="llama3", messages=[{"role": "user", "content": message}])
    
    if response and "message" in response:
        return response["message"].get("content", "Error: No response received")
    return "Error: Llama API did not return a valid response"
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
            bot_response_result = call_aspx_webmethod(bot_response)
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
# if "current_input" not in st.session_state:
#     st.session_state.current_input = ""

# user_input = st.chat_input("Message")

# # Update session state with current input
# if user_input:
#     st.session_state.current_input = user_input 

cols = st.columns([1, 1], gap="small")

with cols[0]: 
    if st.button("Summary"): 
        user_input = st.session_state.get("message")

        if user_input:  # Ensure there's input text
            # Append the user input as a "user" message to the chat history
            st.session_state.chat_history.append({"role": "user", "content": f"Summarize the following: {user_input}"})

            # Call Llama API to generate summary
            bot_response = ollama.chat(model="llama3", messages=[{"role": "user", "content": f"Summarize the following: {user_input}"}]).get("message", {}).get("content", "Error: No response received")

            # Append the bot response (summary) to chat history
            st.session_state.chat_history.append({"role": "assistant", "content": bot_response})
            st.rerun()
        else:
             
            st.warning("Please enter a message before summarizing.")



with cols[1]:
    if st.button("Progress"):
        user_input = "Progress"
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        bot_response = ollama.chat(model="llama3", messages=[{"role": "user", "content": user_input}]).get("message", {}).get("content", "Error: No response received")
        st.session_state.chat_history.append({"role": "assistant", "content": bot_response})
        st.rerun()