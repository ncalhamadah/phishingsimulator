from flask import Flask, request
import requests
import os

app = Flask(__name__)

# Mailtrap Email Sending API Configuration
MAILTRAP_API_TOKEN = "b80afb201f5235f81e13d2928b618006"
FROM_EMAIL = "ithelpdesk@eden.ae"
TO_EMAIL = "it@eden.ae"

def send_email_via_mailtrap_api(hostname, ip, user_agent, extra=None):
    api_url = "https://send.api.mailtrap.io/api/send"

    headers = {
        "Authorization": f"Bearer {MAILTRAP_API_TOKEN}",
        "Content-Type": "application/json"
    }

    data = {
        "from": {"email": FROM_EMAIL},
        "to": [{"email": TO_EMAIL}],
        "subject": "Phishing Simulation: Link Clicked",
        "text": f"""
Phishing simulation link clicked!

Details:
- Hostname: {hostname}
- IP Address: {ip}
- User-Agent: {user_agent}
- Extra Info: {extra if extra else 'N/A'}
"""
    }

    try:
        response = requests.post(api_url, headers=headers, json=data)
        if response.status_code == 200:
            print("✅ Email sent via Mailtrap API")
        else:
            print(f"❌ API Error {response.status_code}: {response.text}")
    except Exception as e:
        print("❌ Request failed:", str(e))

@app.route("/phish", methods=["GET"])
def phishing_endpoint():
    ip = request.remote_addr
    user_agent = request.headers.get("User-Agent", "Unknown")
    hostname = request.args.get("host", "Unknown")
    username = request.args.get("user", "Unknown")

    print(f"🔔 Phishing click - Host: {hostname}, IP: {ip}, User: {username}")
    send_email_via_mailtrap_api(hostname, ip, user_agent, f"user={username}")

    return "<h3 style='color:red;'>Access Denied.</h3>", 403

@app.route("/", methods=["GET"])
def home():
    return "<h3>Phishing Simulation Backend is Running</h3>"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
