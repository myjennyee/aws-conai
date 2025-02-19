import streamlit as st
import requests
import json
import ollama
import pandas as pd
# Streamlit UI Setup
st.set_page_config(page_title="WYT AI", layout="wide")
st.title("🤖 WYT AI")

# Your WebMethod URL (hosted on IIS)
WEBMETHOD_URL = "https://localhost:44355/Forms/Ai.aspx/GetChatbotResponse"  # Change this to your actual ASPX URL
def json_to_html_table(json_data):
        # Start the HTML table
        html_table = "<table border='1'>\n"
        
        # Create headers dynamically
        headers = json_data[0].keys()  # Get the keys of the first dictionary
        html_table += "  <tr>\n"
        for header in headers:
            html_table += f"    <th>{header}</th>\n"
        html_table += "  </tr>\n"
        
        # Create rows dynamically
        for item in json_data:
            html_table += "  <tr>\n"
            for value in item.values():
                # Ensure we handle None or special cases appropriately
                value = value if value is not None else ""
                html_table += f"    <td>{value}</td>\n"
            html_table += "  </tr>\n"
        
        # Close the table
        html_table += "</table>"
        
        return html_table
# Function to call ASPX WebMethod
def call_aspx_webmethod(user_message):
    headers = {"Content-Type": "application/json"}
    payload = {"userMessage": user_message}  # Use the actual input

    try:
        print("📡 Sending request to:", WEBMETHOD_URL)
        print("📨 Payload:", payload)

        response = requests.post(WEBMETHOD_URL, json=payload, headers=headers, verify=False)  # Use json=payload

        #print("📮 Raw Response:", response.text)  # Print raw response for debugging
        return response.text
        #response.raise_for_status()  # Raise error if HTTP response is not 200

        #response_data = response.json()
        #print("✅ Parsed Response:", response_data)

        #return response_data.get("d", "Error: No response received")  # "d" is the standard ASP.NET wrapper
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

# Function to call Llama (Ollama) and generate SQL
def call_llama_api(user_message):
    # We include the table structure and column names to guide Llama
    table_structure = """
    Table_Clash: clashId, orgClashTestId, clashName, clashIssue, clashDistance, clashGrid, clashLevel, clashPointX, clashPointY, clashPointZ, item1, item2, image, deleteFlg, description, createdBy, createdDateTime, updatedBy, updatedDateTime
    Table_ClashTest: clashTestId, clashTestTimeStamp, orgFile, clashTestZone, clashTestName, tolerance, totalClashes, new, active, reviewed, approved, resolved, type, clashes, deleteFlg, comment, createdBy, createdDateTime, updatedBy, updatedDateTime
    Table_Element: elementId, clashId, clashName, orgClashTestId, orgFile, elementItemType, elementCategory, elementFamily, elementType, elementPhase, deleteFlg, comment, createBy, createdDateTime, updatedBy, updatedDateTime
    """

    # Construct the message to pass to Llama for SQL query generation
    message = f"Generate a valid SQL query from the following input: {user_message}. Use the following tables and columns: {table_structure}"

    response = ollama.chat(model="llama3", messages=[{"role": "user", "content": message}])
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

# User Input and Checkbox Area
col1, col2 = st.columns([4, 1])

with col1:
    user_input = st.chat_input("Type your message...")
with col2:
    search_system_data = st.checkbox("Search system data", value=False)  # Default is unchecked

if user_input:
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    
    if search_system_data:
        # If "Search System Data" is checked, generate SQL query
        bot_response = call_llama_api(user_input)
    else:
        # If not checked, use normal Llama response (no SQL)
        bot_response = ollama.chat(model="llama3", messages=[{"role": "user", "content": user_input}]).get("message", {}).get("content", "Error: No response received")
    #if search_system_data == False:
        st.session_state.chat_history.append({"role": "assistant", "content": bot_response})
    
    bot_response_result = None  # Initialize for optional display
    
    if search_system_data:
        with st.spinner("Thinking..."):
            # Call ASPX WebMethod with generated SQL (if applicable)
            bot_response_result = call_aspx_webmethod(bot_response)
    
    # If the ASPX WebMethod returns a valid JSON table
    if bot_response_result and isinstance(bot_response_result, dict):
        try:
        #json_response = {"response": "[{\"elementId\":\"2385302\",\"clashId\":\"0331e862-429b-42a9-a2cf-8262eae65ce7\",\"clashName\":\"Clash2\",\"orgClashTestId\":\"e1543cf7-a4fe-4aaa-a85b-60d9aef6ca92\",\"orgFile\":\"ICN062-HME-30-XX-M3-H-0000.nwc\",\"elementItemType\":\"Item2\",\"elementCategory\":\"Pipes\",\"elementFamily\":\"Pipe Types\",\"elementType\":\"AWS_Pipe_Carbon Steel\",\"elementPhase\":\"Carbon Steel Pipes For Ordinary Piping(KS D 3507)\",\"deleteFlg\":0,\"comment\":null,\"createBy\":null,\"createdDateTime\":\"2025-02-14T02:27:50.75\",\"updatedBy\":null,\"updatedDateTime\":\"2025-02-14T02:27:50.75\"}]"}  # truncated for brevity

# Parse JSON response
            data = json.loads(bot_response_result)  # Convert the string in "response" into a Python list of dictionaries
            print (data)
# Convert to DataFrame
            df = pd.DataFrame(data)

# Generate HTML table
            html_table = df.to_html(index=False, escape=False)  # Convert DataFrame to HTML

# Display the table in Streamlit chat history
            st.session_state.chat_history.append({"role": "assistant", "content": html_table})

# Optionally, display the table in the current Streamlit app
            st.write(html_table, unsafe_allow_html=True)  # Display as HTML in Streamlit
        except Exception as e:
            # Append an error message in case of JSON parsing failure
            st.session_state.chat_history.append({"role": "assistant", "content": f"Error rendering table: {e}"})
    elif bot_response_result:
        #st.write({"role": "assistant", "content": html_table}) 
        
        st.session_state.chat_history.append({"role": "assistant", "content": bot_response_result})
    

    st.rerun()

# Ready Messages Buttons (Moved to below the input box)
st.write("**Quick Messages:**")
cols = st.columns(len(ready_messages))
for i, msg in enumerate(ready_messages):
    if cols[i].button(msg):
        user_input = msg  # Set message from quick reply
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        
        # Skip SQL generation logic for quick replies
        bot_response = ollama.chat(model="llama3", messages=[{"role": "user", "content": user_input}]).get("message", {}).get("content", "Error: No response received")
        
        st.session_state.chat_history.append({"role": "assistant", "content": bot_response})
        
        # Refresh chat immediately
        st.rerun()
 
# Clear Chat Button
if st.button("🗑️ Clear Chat"):
    st.session_state.chat_history = []
    st.rerun()
