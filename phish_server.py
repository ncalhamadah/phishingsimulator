from flask import Flask, request, render_template_string, redirect
import requests
from datetime import datetime
import os

app = Flask(__name__)

# Mailtrap API Config
MAILTRAP_API_TOKEN = "b80afb201f5235f81e13d2928b618006"
FROM_EMAIL = "ithelpdesk@eden.ae"
TO_EMAIL = "it@eden.ae"

def send_simulation_email(subject, body):
    api_url = "https://send.api.mailtrap.io/api/send"
    headers = {
        "Authorization": f"Bearer {MAILTRAP_API_TOKEN}",
        "Content-Type": "application/json"
    }

    data = {
        "from": {"email": FROM_EMAIL},
        "to": [{"email": TO_EMAIL}],
        "subject": subject,
        "text": body
    }

    try:
        response = requests.post(api_url, headers=headers, json=data)
        if response.status_code == 200:
            print("✅ Email sent to Mailtrap")
        else:
            print(f"❌ Mailtrap API Error {response.status_code}: {response.text}")
    except Exception as e:
        print("❌ Failed to send email:", str(e))

@app.route("/login", methods=["GET"])
def show_login():
    return render_template_string("""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Sign in to your account</title>
    <style>
        body { font-family: 'Segoe UI', sans-serif; background-color: #f3f2f1; margin: 0; padding: 0; }
        .container { max-width: 360px; margin: 100px auto; background: #fff; padding: 40px; border-radius: 4px; box-shadow: 0 0 15px rgba(0,0,0,0.1); }
        h2 { color: #0078d4; }
        input[type="email"], input[type="submit"] { width: 100%; padding: 10px; margin-top: 10px; font-size: 16px; }
        input[type="submit"] { background-color: #0078d4; color: white; border: none; cursor: pointer; }
        input[type="submit"]:hover { background-color: #005a9e; }
        .logo { margin-bottom: 20px; }
    </style>
</head>
<body>
    <div class="container">
        <img class="logo" src="https://logincdn.msauth.net/shared/1.0/content/images/microsoft_logo_ee5c8f3fb6248c9712df.svg" alt="Microsoft" width="120">
        <h2>Sign in</h2>
        <form method="POST" action="/login">
            <input type="email" name="email" placeholder="Email, phone, or Skype" required>
            <input type="submit" value="Next">
        </form>
    </div>
</body>
</html>
""")

@app.route("/login", methods=["POST"])
def process_login():
    user_email = request.form.get("email", "Unknown")
    ip = request.remote_addr
    user_agent = request.headers.get("User-Agent", "Unknown")
    hostname = request.args.get("host", "Unknown")
    username = request.args.get("user", "Unknown")
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")

    # Try to get geolocation
    try:
        geo = requests.get(f"https://ipinfo.io/{ip}/json").json()
        location = f"{geo.get('city', 'Unknown')}, {geo.get('region', '')}, {geo.get('country', '')}"
    except:
        location = "Unavailable"

    body = f"""
Microsoft Login Simulation Clicked

Details:
- Timestamp: {timestamp}
- Email Entered: {user_email}
- Hostname: {hostname}
- Username: {username}
- IP: {ip}
- Location: {location}
- User-Agent: {user_agent}
"""

    send_simulation_email("Phishing Login Simulation", body)
    return redirect("/done")

@app.route("/done", methods=["GET"])
def show_thank_you():
    return render_template_string("""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Phishing Simulation Complete</title>
    <style>
        body { font-family: Arial; text-align: center; background-color: #f4f6f9; padding-top: 100px; }
        .card { background: white; display: inline-block; padding: 40px; border-radius: 8px; box-shadow: 0 0 15px rgba(0,0,0,0.1); }
        h2 { color: #dc3545; }
    </style>
</head>
<body>
    <div class="card">
        <h2>This was a Phishing Simulation</h2>
        <p>No credentials were stored.</p>
        <pThis exercise is part of your organization’s security awareness training.</p>
        <p>If you have concerns, contact IT.</p>
    </div>
</body>
</html>
""")

@app.route("/", methods=["GET"])
def health_check():
    return "<h3>Phishing Simulator is Live</h3>"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
