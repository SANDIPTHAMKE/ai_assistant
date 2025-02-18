from flask import Flask, request, jsonify
import openai

app = Flask(__name__)

# Replace with your OpenAI API key
openai.api_key = "your_openai_api_key"

@app.route("/process", methods=["POST"])
def process():
    data = request.get_json()
    user_text = data.get("text")

    # Generate AI response (You can replace this with any AI model)
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": user_text}]
    )

    ai_reply = response["choices"][0]["message"]["content"]
    return jsonify({"reply": ai_reply})

if __name__ == "__main__":
    app.run(debug=True)
