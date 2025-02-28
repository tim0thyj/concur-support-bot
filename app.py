from flask import Flask, request, jsonify, render_template
import json
from fuzzywuzzy import process

app = Flask(__name__)

# Load Concur knowledge base
with open("concur_data.json", "r") as file:
    knowledge_base = json.load(file)

# Load Concur guides
with open("concur_guides.json", "r") as file:
    concur_guides = json.load(file)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    user_question = request.form["question"].lower()

    # Easter Egg Response
    if "who made you" in user_question:
        return jsonify({"answer": "I was created by a genius named Timothy! 😎"})

    # Search in the knowledge base
    for topic, answer in knowledge_base.items():
        if any(word in user_question for word in topic.lower().split()):
            return jsonify({"answer": answer})

    # Check for related guides from the Concur website
    best_match, score = process.extractOne(user_question, concur_guides.keys())
    if score > 60:
        guide_url = concur_guides[best_match]
        return jsonify({"answer": f"I found a guide that might help: <a href='{guide_url}' target='_blank'>{best_match}</a>"})

    # If no answer is found, provide a general help link
    return jsonify({"answer": "I'm not sure about that. You can find more information here: <a href='https://csuf-afit.screenstepslive.com/m/75002' target='_blank'>Concur Documentation</a>"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

