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

    # Define the list of common questions
    common_questions = [
        "Logging into Concur",
        "Accessing the Concur Menu",
        "Approval Status Check",
        "Concur Attachments",
        "Removing Expense Reports"
    ]

    # Feature: Show the top 5 common questions
    if "five most common questions" in user_question or "top 5 questions" in user_question:
        response_text = "Here are the five most common questions:<br><ul>"
        for question in common_questions:
            if question in concur_guides:
                response_text += f"<li><a href='{concur_guides[question]}' target='_blank'>{question}</a></li>"
        response_text += "</ul>"
        return jsonify({"answer": response_text})

    # Search for an answer in the knowledge base
    for topic, answer in knowledge_base.items():
        if any(word in user_question for word in topic.lower().split()):
            return jsonify({"answer": answer})

    # Check for related guides
    for guide_title, guide_url in concur_guides.items():
        if any(word in user_question for word in guide_title.lower().split()):
            return jsonify({"answer": f"I found a guide that might help: <a href='{guide_url}' target='_blank'>{guide_title}</a>"})

    # If no answer is found, provide a general help link
    return jsonify({"answer": "I'm not sure about that. You can find more information here: <a href='https://csuf-afit.screenstepslive.com/m/75002' target='_blank'>Concur Documentation</a>"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

