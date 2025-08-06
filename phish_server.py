from flask import Flask, request
import smtplib
from email.message import EmailMessage

app = Flask(__name__)

# Mailtrap SMTP configuration
SMTP_SERVER = "live.smtp.mailtrap.io"
SMTP_PORT = 587
SMTP_USER = "api"
SMTP_PASS = "fb46aa750cfdb994564a2208045c50ba"
FROM_ADDRESS = "ithelpdesk@eden.ae"
TO_ADDRESS = "ithelpdesk.eden@edenglobalinvestments.rmmservice.eu"

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
            print("Notification sent.")
    except Exception as e:
        print("Failed to send email:", str(e))

@app.route("/phish", methods=["GET"])
def phishing_endpoint():
    ip = request.remote_addr
    user_agent = request.headers.get("User-Agent", "Unknown")
    hostname = request.args.get("host", "Unknown")
    username = request.args.get("user", "Unknown")

    # Log to console
    print(f"Phishing click - Host: {hostname}, IP: {ip}, User: {username}, UA: {user_agent}")

    # Send email alert
    send_email_notification(hostname, ip, user_agent, f"user={username}")

    return "<h3 style='color:red;'>Access Denied.</h3>", 403

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
