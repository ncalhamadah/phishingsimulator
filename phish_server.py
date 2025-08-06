from flask import Flask, request
import smtplib
from email.message import EmailMessage
import os

app = Flask(__name__)

# Mailtrap SMTP Configuration (Update if you're using Microsoft SMTP)
SMTP_SERVER = "live.smtp.mailtrap.io"
SMTP_PORT = 587
SMTP_USER = "api"
SMTP_PASS = "fb46aa750cfdb994564a2208045c50ba"
FROM_ADDRESS = "ithelpdesk@eden.ae"
TO_ADDRESS = "it@eden.ae"  # 👈 Updated here

def send_email_notification(hostname, ip, user_agent, extra=None):
    subject = "Phishing Simulation: Link Clicked"
    body = f"""
Phishing simulation link clicked!

Details:
- Hostname: {hostname}
- IP Address: {ip}
- User-Agent: {user_agent}
- Extra Info: {extra if extra else 'N/A'}
"""

    msg = EmailMessage()
    msg.set_content(body)
    msg["Subject"] = subject
    msg["From"] = FROM_ADDRESS
    msg["To"] = TO_ADDRESS

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASS)
            server.send_message(msg)
            print("✅ Email sent to", TO_ADDRESS)
    except Exception as e:
        print("❌ SMTP Error:", str(e))

@app.route("/phish", methods=["GET"])
def phishing_endpoint():
    ip = request.remote_addr
    user_agent = request.headers.get("User-Agent", "Unknown")
    hostname = request.args.get("host", "Unknown")
    username = request.args.get("user", "Unknown")

    print(f"🔔 Phishing click detected - Host: {hostname}, IP: {ip}, User: {username}, UA: {user_agent}")
    send_email_notification(hostname, ip, user_agent, f"user={username}")

    return "<h3 style='color:red;'>Access Denied.</h3>", 403

# Optional homepage route
@app.route("/", methods=["GET"])
def home():
    return "<h3>Phishing Simulation Backend is Running</h3>"

# Auto-bind port for Render
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
