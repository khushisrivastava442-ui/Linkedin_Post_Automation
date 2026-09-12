from flask import Flask, render_template, redirect, request, session
from dotenv import load_dotenv
import os
import requests

load_dotenv()

app = Flask(__name__)
app.secret_key = "linkedin-post-automation-secret"
CLIENT_ID = os.getenv("LINKEDIN_CLIENT_ID")
CLIENT_SECRET = os.getenv("LINKEDIN_CLIENT_SECRET")

REDIRECT_URI = "http://127.0.0.1:5000/callback"


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/login")
def login():
    linkedin_url = (
        "https://www.linkedin.com/oauth/v2/authorization"
        f"?response_type=code"
        f"&client_id={CLIENT_ID}"
        f"&redirect_uri={REDIRECT_URI}"
        f"&scope=w_member_social"
    )

    return redirect(linkedin_url)


@app.route("/callback")
def callback():
    code = request.args.get("code")

    if not code:
        return "Authorization failed."

    token_url = "https://www.linkedin.com/oauth/v2/accessToken"

    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET
    }

    response = requests.post(token_url, data=data)

    if response.status_code != 200:
        return f"Token error: {response.text}"

    token_data = response.json()
    session["access_token"] = token_data.get("access_token")
    access_token = token_data.get("access_token")

    return f"""
    <h2>LinkedIn Connected Successfully! ✅</h2>
    <p>Access token received.</p>
    <p>Now go back to the home page:</p>
    <a href="/">Create LinkedIn Post</a>
    """


if __name__ == "__main__":
    app.run(debug=True)