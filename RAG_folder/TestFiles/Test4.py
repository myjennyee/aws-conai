import requests
import json

# Your ASPX WebMethod URL (Ensure it's the correct one)
WEBMETHOD_URL = "https://localhost:44355/Forms/Ai.aspx/GetChatbotResponse"

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

# 🔬 **Test the function**
test_message = "Hello, ASPX!"
print(call_aspx_webmethod(test_message))
