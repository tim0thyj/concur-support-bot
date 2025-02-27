from flask import Flask, request, jsonify, render_template
import json

app = Flask(__name__)

# Load Concur knowledge base from a JSON file
with open("concur_data.json", "r") as file:
    knowledge_base = json.load(file)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    user_question = request.form["question"].lower()

    # Simple keyword search
    for topic, answer in knowledge_base.items():
        if any(word in user_question for word in topic.lower().split()):
            return jsonify({"answer": answer})

    return jsonify({"answer": "Sorry, I don't have an answer for that. Please check Concur documentation: https://csuf-afit.screenstepslive.com/m/75002."})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

