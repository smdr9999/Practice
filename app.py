import os
import smtplib
from flask import Flask, request, jsonify
from email.mime.text import MIMEText
from email.utils import formataddr

app = Flask(__name__)

@app.route('/')
def home():
    return "Gmail Email API is active."

@app.route('/send', methods=['POST'])
def send_email():
    data = request.get_json()
    text = data.get("text", "")

    from_email = os.environ["EMAIL_FROM"].strip()
    to_email = os.environ["EMAIL_TO"].strip()[1:]

    msg = MIMEText(text)
    msg["Subject"] = "Typed Data"
    msg["From"] = formataddr(("Sender", from_email))
    msg["To"] = formataddr(("Recipient", to_email))

    print(f"EMAIL_TO (raw): {os.environ['EMAIL_TO']}")
    print(f"EMAIL_TO (repr): {repr(to_email)}")
    print(f"msg['To']: {msg['To']}")
    print(f"Full email message:\n{msg.as_string()}")

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(from_email, os.environ["EMAIL_PASSWORD"])
            server.send_message(msg)
        return jsonify({"status": "Email sent"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
