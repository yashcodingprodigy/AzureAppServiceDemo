from flask import Flask, request, abort
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
import os

app = Flask(__name__)

# Your Key Vault URL (replace with yours)
KEY_VAULT_URL = "https://yashkeyvaultverysafe.vault.azure.net/"

# Initialize Key Vault client with managed identity
credential = DefaultAzureCredential()
client = SecretClient(vault_url=KEY_VAULT_URL, credential=credential)

@app.route("/")
def home():
    try:
        # Get secret from Key Vault (executed at request-time, not startup)
        retrieved_secret = client.get_secret("app-auth-secret").value

        # Get API key from incoming request
        api_key = request.headers.get('x-api-key')

        # If API key is missing or incorrect, deny access
        if api_key != retrieved_secret:
            abort(403, "Invalid API key")

        return "✅ Authorized! Access granted."

    except Exception as e:
        return f"❌ Error: {str(e)}", 500

@app.route("/ping")
def ping():
    return "✅ App is running!"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)
