from flask import Flask, request, render_template_string, redirect
import requests
from datetime import datetime
import os

app = Flask(__name__)

# Mailtrap API Config
MAILTRAP_API_TOKEN = "b80afb201f5235f81e13d2928b618006"
FROM_EMAIL = "ithelpdesk@eden.ae"
TO_EMAIL = "phishingcampaign@edenglobalinvestments.rmmservice.eu"

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
    # Get host and user from query string to preserve through POST
    host = request.args.get("host", "Unknown")
    user = request.args.get("user", "Unknown")
    # Microsoft 365 styled login page with updated logo
    return render_template_string(f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <meta http-equiv="X-UA-Compatible" content="IE=edge" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Sign in to your account</title>
    <style>
        body {{ margin:0; padding:0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f3f2f1; }}
        .main {{ display:flex; align-items:center; justify-content:center; height:100vh; }}
        .login-box {{ width:360px; background-color:#fff; padding:30px 40px; border:1px solid #c8c6c4; border-radius:4px; box-shadow:0 4px 8px rgba(0,0,0,0.1); }}
        .logo {{ display:block; margin:0 auto 20px; }}
        h1 {{ font-size:24px; font-weight:normal; color:#323130; text-align:center; margin:0 0 20px; }}
        input[type="email"] {{ width:100%; padding:10px; font-size:14px; border:1px solid #bebebe; border-radius:2px; margin-bottom:20px; }}
        input[type="submit"] {{ width:100%; padding:10px; font-size:16px; color:#fff; background-color:#0078d4; border:1px solid #0078d4; border-radius:2px; cursor:pointer; }}
        input[type="submit"]:hover {{ background-color:#005a9e; border-color:#005a9e; }}
        .footer {{ font-size:12px; color:#605e5c; text-align:center; margin-top:20px; }}
        .footer a {{ color:#0078d4; text-decoration:none; }}
    </style>
</head>
<body>
    <div class="main">
        <div class="login-box">
            <img class="logo" src="https://upload.wikimedia.org/wikipedia/commons/thumb/4/44/Microsoft_logo.svg/1200px-Microsoft_logo.svg.png" alt="Microsoft logo" width="80" />
            <h1>Sign in to your account</h1>
            <form method="POST" action="/login?host={host}&user={user}">
                <input type="email" name="email" placeholder="Email, phone, or Skype" required autofocus />
                <input type="submit" value="Next" />
            </form>
            <div class="footer">
                <p>Use your work or school account.</p>
                <p><a href="https://support.microsoft.com/">Can't access your account?</a></p>
            </div>
        </div>
    </div>
</body>
</html>
"""
)

@app.route("/login", methods=["POST"])
def process_login():
    user_email = request.form.get("email", "Unknown")
    ip = request.remote_addr
    user_agent = request.headers.get("User-Agent", "Unknown")
    hostname = request.args.get("host", "Unknown")
    username = request.args.get("user", "Unknown")
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")

    # Geo IP lookup
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
    # Professional awareness page
    return render_template_string("""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Phishing Simulation Complete</title>
    <style>
        body { background-color: #f4f6f9; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; display:flex; align-items:center; justify-content:center; height:100vh; margin:0; }
        .card { background: white; padding: 40px; border-radius: 8px; box-shadow: 0 0 15px rgba(0,0,0,0.1); text-align:center; width:420px; }
        h2 { color: #323130; margin-bottom:20px; }
        p { color: #605e5c; font-size:14px; margin:10px 0; }
        a { color: #0078d4; text-decoration:none; }
    </style>
</head>
<body>
    <div class="card">
        <h2>This was a Phishing Simulation</h2>
        <p><strong>No credentials were stored.</strong></p>
        <p>This exercise is part of your organization’s security awareness training.</p>
        <p>If you have concerns, <a href="mailto:it@eden.ae">contact IT</a>.</p>
    </div>
</body>
</html>
"""
)

@app.route("/", methods=["GET"])
def health_check():
    return "<h3>Phishing Simulator is Live</h3>"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

