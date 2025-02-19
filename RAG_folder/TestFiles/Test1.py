import requests
import json

class LlamaClient:
    def __init__(self, base_url):
        self.base_url = base_url

    def send_to_llama(self, question):
        # API endpoint
        url = f"{self.base_url}/api/chat"

        # Request body
        request_body = {
            "model": "llama3",  # Replace with the correct model name
            "messages": [
                {"role": "user", "content": question}
            ]
        }

        # Headers
        headers = {
            "Content-Type": "application/json"
        }

        try:
            # Make POST request
            response = requests.post(url, data=json.dumps(request_body), headers=headers)

            # Check if the response was successful
            if response.status_code == 200:
                return response  # Return the parsed JSON response
            else:
                # Log error details if not successful
                return f"Error: {response.status_code}, Details: {response.text}"

        except requests.exceptions.RequestException as e:
            # Handle any exceptions
            return f"Exception occurred: {str(e)}"


# Example usage:
if __name__ == "__main__":
    llama_client = LlamaClient(base_url="http://localhost:11434")  # Replace with your server URL

    # Send a question to the Llama model
    question = "Hello, how are you?"
    result = llama_client.send_to_llama(question)

    print("Response from Llama:")
    print(result.text)
