from flask import Flask, request, jsonify, render_template
import json

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

    # Check the knowledge base first
    for topic, answer in knowledge_base.items():
        if any(word in user_question for word in topic.lower().split()):
            return jsonify({"answer": answer})

    # If no direct answer, check for related guides
    for guide_title, guide_url in concur_guides.items():
        if any(word in user_question for word in guide_title.lower().split()):
            return jsonify({"answer": f"I found a guide that might help: {guide_title}. You can view it here: {guide_url}"})

    # If no answer found
    return jsonify({"answer": "Sorry, I couldn't find an answer. Try checking the Concur documentation at https://csuf-afit.screenstepslive.com/m/75002."})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

