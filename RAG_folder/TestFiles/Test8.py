import streamlit as st
import requests
import json
import ollama
import pandas as pd

# Streamlit UI Setup
# st.set_page_config(page_title="WYT AI", layout="wide")
# st.title("WYT AI Chatbot")

# Your WebMethod URL (hosted on IIS)
WEBMETHOD_URL = "https://localhost:44355/Forms/Ai.aspx/GetChatbotResponse"  # Change this to your actual ASPX URL

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

def call_llama_api(user_message):
    table_structure = """
    Table_Clash: clashId, orgClashTestId, clashName, clashIssue, clashDistance, clashGrid, clashLevel, clashPointX, clashPointY, clashPointZ, item1, item2, image, deleteFlg, description, createdBy, createdDateTime, updatedBy, updatedDateTime
    Table_ClashTest: clashTestId, clashTestTimeStamp, orgFile, clashTestZone, clashTestName, tolerance, totalClashes, new, active, reviewed, approved, resolved, type, clashes, deleteFlg, comment, createdBy, createdDateTime, updatedBy, updatedDateTime
    Table_Element: elementId, clashId, clashName, orgClashTestId, orgFile, elementItemType, elementCategory, elementFamily, elementType, elementPhase, deleteFlg, comment, createBy, createdDateTime, updatedBy, updatedDateTime
    """
    message = f"Generate a valid SQL query from the following input: {user_message}. Use the following tables and columns: {table_structure}"
    response = ollama.chat(model="llama3", messages=[{"role": "user", "content": message}])
    return response.get("message", {}).get("content", "Error: No response received")

# Chat Display
for chat in st.session_state.chat_history:
    role = "User" if chat["role"] == "user" else "Bot"
    st.markdown(f"**{role}:** {chat['content']}")

# User Input Area
user_input = st.chat_input("Type your message...")
search_system_data = st.checkbox("Search system data", value=False)

if user_input:
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    
    if search_system_data:
        bot_response = call_llama_api(user_input)
    else:
        bot_response = ollama.chat(model="llama3", messages=[{"role": "user", "content": user_input}]).get("message", {}).get("content", "Error: No response received")
    
    st.session_state.chat_history.append({"role": "assistant", "content": bot_response})
    
    if search_system_data:
        with st.spinner("Processing..."):
            bot_response_result = call_aspx_webmethod(bot_response)
        
        try:
            data = json.loads(bot_response_result)
            df = pd.DataFrame(data)
            html_table = df.to_html(index=False, escape=False)
            st.session_state.chat_history.append({"role": "assistant", "content": html_table})
            st.write(html_table, unsafe_allow_html=True)
        except Exception as e:
            st.session_state.chat_history.append({"role": "assistant", "content": f"Error rendering table: {e}"})
    
    st.rerun()

# Action Buttons
col1, col2 = st.columns(2)
if col1.button("Summary"):
    st.session_state.chat_history.append({"role": "user", "content": "Summary"})
    summary_response = ollama.chat(model="llama3", messages=[{"role": "user", "content": "Provide a summary."}]).get("message", {}).get("content", "Error: No response received")
    st.session_state.chat_history.append({"role": "assistant", "content": summary_response})
    st.rerun()

if col2.button("Progress"):
    st.session_state.chat_history.append({"role": "user", "content": "Progress"})
    progress_response = ollama.chat(model="llama3", messages=[{"role": "user", "content": "Provide progress details."}]).get("message", {}).get("content", "Error: No response received")
    st.session_state.chat_history.append({"role": "assistant", "content": progress_response})
    st.rerun()

# Clear Chat Button
if st.button("Clear Chat"):
    st.session_state.chat_history = []
    st.rerun()
