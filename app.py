import os
import webbrowser
import pyautogui
import time
from flask import Flask, request, jsonify
import openai

app = Flask(__name__)

# Replace with your OpenAI API key
openai.api_key = "your_openai_api_key"

# System app commands (Modify if needed)
APP_COMMANDS = {
    "notepad": "notepad" if os.name == "nt" else "gedit",
    "calculator": "calc" if os.name == "nt" else "gnome-calculator",
    "terminal": "cmd" if os.name == "nt" else "gnome-terminal",
    "browser": "start chrome" if os.name == "nt" else "firefox",
    "word": "start winword",
    "excel": "start excel",
    "powerpoint": "start powerpnt"
}

# List of common websites
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
    for site in WEBSITES:
        if f"open {site}" in user_text:
            webbrowser.open(WEBSITES[site])
            return jsonify({"reply": f"Opening {site}..."})

    # Open a system app
    for app in APP_COMMANDS:
        if f"open {app}" in user_text:
            os.system(APP_COMMANDS[app])
            return jsonify({"reply": f"Opening {app}..."})

    # Start live dictation in Word
    if "start dictation" in user_text:
        os.system(APP_COMMANDS["word"])  # Open Word
        time.sleep(5)  # Wait for Word to open
        pyautogui.hotkey("win", "h")  # Open Windows speech-to-text
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
