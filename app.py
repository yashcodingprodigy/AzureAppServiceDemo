from flask import Flask
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
import os

app = Flask(__name__)

KEY_VAULT_URL = "https://yashkeyvaultverysafe.vault.azure.net/"
credential = DefaultAzureCredential()
client = SecretClient(vault_url=KEY_VAULT_URL, credential=credential)

@app.route("/")
def home():
    try:
        # Try to access a secret from Key Vault
        secret_value = client.get_secret("app-auth-secret").value

        return f"✅ Welcome! Secret loaded from Key Vault: {secret_value}"

    except Exception as e:
        return f"❌ Access denied or error reading from Key Vault:<br><br>{str(e)}", 500

@app.route("/ping")
def ping():
    return "✅ App is running!"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)
