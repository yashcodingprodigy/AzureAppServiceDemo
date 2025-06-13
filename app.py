from flask import Flask, request, abort
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
import os

app = Flask(__name__)

# Key Vault URL
KEY_VAULT_URL = "https://yashkeyvaultverysafe.vault.azure.net/"

# Set up Azure Key Vault client
credential = DefaultAzureCredential()
client = SecretClient(vault_url=KEY_VAULT_URL, credential=credential)

@app.route("/")
def home():
    try:
        # Fetch secret inside the route
        retrieved_secret = client.get_secret("app-auth-secret").value
        api_key = request.headers.get('x-api-key')
        if api_key != retrieved_secret:
            abort(403)
        return "✅ Authorized! You accessed a secure route."
    except Exception as e:
        return f"❌ Error: {str(e)}", 500

@app.route("/ping")
def ping():
    return "App is alive!"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)
