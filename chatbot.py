import json
import random
import pickle

model = pickle.load(open("model.pkl", "rb"))
vectorizer = pickle.load(open("vectorizer.pkl", "rb"))

with open("intents.json") as file:
    data = json.load(file)

while True:
    user = input("You: ")

    X = vectorizer.transform([user])
    tag = model.predict(X)[0]

    for intent in data["intents"]:
        if intent["tag"] == tag:
            print("Bot:", random.choice(intent["responses"]))