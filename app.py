from flask import Flask, request, jsonify, render_template
import json
from fuzzywuzzy import fuzz

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

    best_match = None
    highest_score = 0

    # Check for the best match in the knowledge base
    for topic, answer in knowledge_base.items():
        score = fuzz.partial_ratio(user_question, topic.lower())
        if score > highest_score:
            highest_score = score
            best_match = answer

    # If confidence is high, return the best match
    if highest_score > 70:  # Only return if similarity score is above 70%
        return jsonify({"answer": best_match})

    # If no match, check for related guides
    for guide_title, guide_url in concur_guides.items():
        if fuzz.partial_ratio(user_question, guide_title.lower()) > 70:
            return jsonify({"answer": f"I found a guide that might help: <a href='{guide_url}' target='_blank'>{guide_title}</a>"})

    # If no answer found, provide the main documentation link
    return jsonify({"answer": "I'm not sure about that. You can find more information here: <a href='https://csuf-afit.screenstepslive.com/m/75002' target='_blank'>Concur Documentation</a>"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

