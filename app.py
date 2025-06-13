from flask import Flask, request, abort
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
import os

app = Flask(__name__)

# Key Vault URL (replace with yours)
KEY_VAULT_URL = "https://yashkeyvaultverysafe.vault.azure.net/"

# Set up Azure Key Vault client
credential = DefaultAzureCredential()
client = SecretClient(vault_url=KEY_VAULT_URL, credential=credential)

# Get secret from Key Vault
retrieved_secret = client.get_secret("app-auth-secret").value

@app.route("/")
def home():
    # Check if 'x-api-key' header matches the secret
    api_key = request.headers.get('x-api-key')
    if api_key != retrieved_secret:
        abort(403)  # Forbidden
    return "✅ Authorized! You accessed a secure route."

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)
