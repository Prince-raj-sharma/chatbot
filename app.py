from flask import Flask, request, jsonify
import pickle
import json
import random

app = Flask(__name__)

model = pickle.load(open("model.pkl", "rb"))
vectorizer = pickle.load(open("vectorizer.pkl", "rb"))

with open("intents.json") as file:
    data = json.load(file)

@app.route("/")
def home():
    return "Chatbot is running"

@app.route("/chat", methods=["POST"])
def chat():
    message = request.json["message"]

    X = vectorizer.transform([message])
    tag = model.predict(X)[0]

    for intent in data["intents"]:
        if intent["tag"] == tag:
            response = random.choice(intent["responses"])

    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)