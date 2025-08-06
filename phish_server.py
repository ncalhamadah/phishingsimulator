from flask import Flask, request
import requests
from datetime import datetime
import os

app = Flask(__name__)

# Mailtrap Email Sending API Configuration
MAILTRAP_API_TOKEN = "b80afb201f5235f81e13d2928b618006"
FROM_EMAIL = "ithelpdesk@eden.ae"
TO_EMAIL = "it@eden.ae"

def send_email_via_mailtrap_api(hostname, ip, user_agent, username):
    api_url = "https://send.api.mailtrap.io/api/send"
    headers = {
        "Authorization": f"Bearer {MAILTRAP_API_TOKEN}",
        "Content-Type": "application/json"
    }

    # Get timestamp
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")

    # Optional: Geo IP Lookup
    try:
        geo = requests.get(f"https://ipinfo.io/{ip}/json").json()
        location = f"{geo.get('city', 'Unknown')}, {geo.get('region', '')}, {geo.get('country', '')}"
    except Exception:
        location = "Unavailable"

    email_body = f"""
Phishing simulation link clicked!

Details:
- Timestamp: {timestamp}
- Hostname: {hostname}
- Username: {username}
- IP Address: {ip}
- Location: {location}
- User-Agent: {user_agent}
"""

    data = {
        "from": {"email": FROM_EMAIL},
        "to": [{"email": TO_EMAIL}],
        "subject": "Phishing Simulation: Link Clicked",
        "text": email_body
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

    print(f"🔔 Click detected - Host: {hostname}, IP: {ip}, User: {username}")
    send_email_via_mailtrap_api(hostname, ip, user_agent, username)

    # Landing page message
    return """
    <html>
    <head>
        <style>
            body {
                background-color: #f8f9fa;
                font-family: Arial, sans-serif;
                text-align: center;
                padding-top: 80px;
                color: #343a40;
            }
            .container {
                background: white;
                display: inline-block;
                padding: 40px;
                border-radius: 8px;
                box-shadow: 0 0 20px rgba(0,0,0,0.1);
            }
            h1 {
                color: #dc3545;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Phishing Simulation Test</h1>
            <p>This was a simulated phishing email conducted by your organization.</p>
            <p><strong>No harm</strong> has been done to your machine.</p>
            <p>Your action was recorded as part of our <strong>security awareness training</strong>.</p>
            <p>If you have any questions, please contact your IT department.</p>
        </div>
    </body>
    </html>
    """, 200


@app.route("/", methods=["GET"])
def home():
    return "<h3>Phishing Simulation Backend is Running</h3>"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
