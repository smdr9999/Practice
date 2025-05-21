import os
import smtplib
from flask import Flask, request, jsonify
from email.mime.text import MIMEText

app = Flask(__name__)

@app.route('/')
def home():
    return "Gmail Email API is active."

@app.route('/send', methods=['POST'])
def send_email():
    data = request.get_json()
    text = data.get("text", "")

    msg = MIMEText(text)
    msg["Subject"] = "Typed Data"
    msg["From"] = os.environ["EMAIL_FROM"]
    msg["To"] = os.environ["EMAIL_TO"]

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(os.environ["EMAIL_FROM"], os.environ["EMAIL_PASSWORD"])
            server.send_message(msg)
        return jsonify({"status": "Email sent to"+msg["To"]}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
