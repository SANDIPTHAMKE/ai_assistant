import os
import webbrowser
import subprocess
import pyautogui
import time
from flask import Flask, request, jsonify
import openai

app = Flask(__name__)

openai.api_key = "your_openai_api_key"

# System app commands (Modify paths if needed)
APP_COMMANDS = {
    "word": "C:\\Program Files\\Microsoft Office\\root\\Office16\\WINWORD.EXE",
    "excel": "C:\\Program Files\\Microsoft Office\\root\\Office16\\EXCEL.EXE",
    "powerpoint": "C:\\Program Files\\Microsoft Office\\root\\Office16\\POWERPNT.EXE",
    "notepad": "notepad",
    "calculator": "calc",
    "terminal": "cmd"
}

# Common website URLs
WEBSITES = {
    "google": "https://www.google.com",
    "youtube": "https://www.youtube.com",
    "github": "https://www.github.com",
    "facebook": "https://www.facebook.com",
    "twitter": "https://www.twitter.com"
}

@app.route("/process", methods=["POST"])
def process():
    data = request.get_json()
    user_text = data.get("text").lower()

    # Open a website
    for site, url in WEBSITES.items():
        if f"open {site}" in user_text:
            webbrowser.open(url)
            return jsonify({"reply": f"Opening {site}..."})

    # Open a system app
    for app, command in APP_COMMANDS.items():
        if f"open {app}" in user_text:
            subprocess.Popen(command, shell=True)  # Use subprocess instead of os.system
            return jsonify({"reply": f"Opening {app}..."})

    # Start live dictation in Word
    if "start dictation" in user_text:
        subprocess.Popen(APP_COMMANDS["word"], shell=True)  # Open Word
        time.sleep(5)  # Wait for Word to open
        pyautogui.hotkey("win", "h")  # Start Windows speech-to-text
        return jsonify({"reply": "Starting live dictation in Word..."})

    # Use AI for general responses
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": user_text}]
    )

    ai_reply = response["choices"][0]["message"]["content"]
    return jsonify({"reply": ai_reply})

if __name__ == "__main__":
    app.run(debug=True)
