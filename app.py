from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello Yash from Azure Web App running Python 3.13!"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)
