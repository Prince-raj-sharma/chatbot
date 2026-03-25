from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)

# Admin Login Credentials
USERNAME = "raj45prince"
PASSWORD = "piyush@123"

# Login Route
@app.route("/admin/login", methods=["POST"])
def login():
    data = request.json

    if data["username"] == USERNAME and data["password"] == PASSWORD:
        return jsonify({"message": "Login successful"})
    else:
        return jsonify({"message": "Invalid credentials"})

# Train Route
@app.route("/admin/train", methods=["POST"])
def train():

    data = request.json

    tag = data["tag"]
    pattern = data["pattern"]
    response = data["response"]

    with open("intents.json") as file:
        intents = json.load(file)

    # Check if tag exists
    for intent in intents["intents"]:
        if intent["tag"] == tag:
            intent["patterns"].append(pattern)
            intent["responses"].append(response)
            break
    else:
        intents["intents"].append({
            "tag": tag,
            "patterns": [pattern],
            "responses": [response]
        })

    with open("intents.json", "w") as file:
        json.dump(intents, file, indent=2)

    # Retrain model
    os.system("python3 train.py")

    return jsonify({"message": "Training complete"})


if __name__ == "__main__":
    app.run(debug=True)