# Function to call Llama for SQL generation
import json
import ollama
import requests
# Table structure for SQL generation
table_structure = """
Table_Clash: clashId, orgClashTestId, clashName, clashIssue, clashDistance, clashGrid, clashLevel, clashPointX, clashPointY, clashPointZ, item1, item2, image, deleteFlg, description, createdBy, createdDateTime, updatedBy, updatedDateTime
Table_ClashTest: clashTestId, clashTestTimeStamp, orgFile, clashTestZone, clashTestName, tolerance, totalClashes, new, active, reviewed, approved, resolved, type, clashes, deleteFlg, comment, createdBy, createdDateTime, updatedBy, updatedDateTime
Table_Element: elementId, clashId, clashName, orgClashTestId, orgFile, elementItemType, elementCategory, elementFamily, elementType, elementPhase, deleteFlg, comment, createBy, createdDateTime, updatedBy, updatedDateTime
"""
BASE_URL = "https://localhost:44355/Forms/Ai.aspx/"  # Change this to actual URL
# Function to call ASPX WebMethod API
def call_aspx_webmethod(user_message):
    headers = {"Content-Type": "application/json"}
    payload = {"userMessage": user_message}
    try:
        response = requests.post(BASE_URL+"GetChatbotResponse", json=payload, headers=headers, verify=False)
        return response.text
    except requests.exceptions.RequestException as e:
        return f"Error: {e}"
    
def call_llama_api_system(user_message):
    message = f"Generate a valid SQL query from the following input: {user_message}. Use the following tables and columns: {table_structure}"
    response = ollama.chat(model="llama3", messages=[{"role": "user", "content": message}])
    
    if response and "message" in response:
        return response["message"].get("content", "Error: No response received")
    return "Error: Llama API did not return a valid response"
 
def call_llama_api(user_message):
    response = ollama.chat(model="llama3", messages=[{"role": "user", "content": user_message}])
    
    if response and "message" in response:
        return response["message"].get("content", "Error: No response received")
    return "Error: Llama API did not return a valid response"

def save_chat_message(userId, role, message):
    headers = {"Content-Type": "application/json"}
    payload = {"userId": userId, "role":role, "message":message}
    try:
        response =requests.post(BASE_URL+"SaveChatMessage", json=payload, headers=headers, verify=False)
        return response.text
    except requests.exceptions.RequestException as er:
        return f"Error: {er}"

def get_chat_history(userId):
    headers = {"Content-Type": "application/json"}
    payload = {"userId": userId }
    try:
        response =requests.post(BASE_URL+"GetChatHistory", json=payload, headers=headers, verify=False)
         
     # Convert response.text (string) to a dictionary
        response_dict = json.loads(response.text)  # Convert JSON string to Python dict

    # Now safely access "d"
        encoded_json_string = response_dict["d"]  # Extract JSON string from "d"

    # Decode the double-encoded JSON
        decoded_json_string = json.loads(encoded_json_string)  # Decode once
        chat_history = json.loads(decoded_json_string)  # Decode again to get a list
        
        return chat_history
    except requests.exceptions.RequestException as er:
        return f"Error: {er}"

