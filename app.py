from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# A list to store chat messages
chat_history = []

@app.route("/")
def index():
    return render_template("index.html", chat=chat_history)

@app.route("/send_message", methods=["POST"])
def send_message():
    message = request.form.get("message")
    if message:
        chat_history.append(message)
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(debug=True)
