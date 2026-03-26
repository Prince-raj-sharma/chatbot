from flask import Flask, request, jsonify
import pickle
import json
import random
import os

app = Flask(__name__)

# Load model and vectorizer
model = pickle.load(open("model.pkl", "rb"))
vectorizer = pickle.load(open("vectorizer.pkl", "rb"))

# Load intents
with open("intents.json") as file:
    data = json.load(file)

# Home route
@app.route("/")
def home():
    return "Chatbot is running"

# Chat route
@app.route("/chat", methods=["POST"])
def chat():
    message = request.json["message"]

    X = vectorizer.transform([message])
    tag = model.predict(X)[0]

    response = "Sorry, I didn't understand"

    for intent in data["intents"]:
        if intent["tag"] == tag:
            response = random.choice(intent["responses"])
            break

    return jsonify({"response": response})

# Run app
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Local 5000, Render auto
    app.run(host="0.0.0.0", port=port)