from flask import Flask, render_template, request, session
from flask_session import Session

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


def get_response(user_input):
    user_input = user_input.lower()
    responses = {
        ("hello", "hi", "hey"): "Hello! How can I help you today?",
        ("how are you", "how do you do"): "I'm just a program, but I'm doing fine! Thanks for asking.",
        ("your name", "who are you"): "I'm your friendly AI ChatBox on the web!",
        ("bye", "goodbye", "exit"): "Goodbye! Have a great day.",
        ("thank you", "thanks"): "You're welcome!",
        ("help", "support"): "Sure, tell me what you need help with."
    }

    for keywords, reply in responses.items():
        for keyword in keywords:
            if keyword in user_input:
                return reply

    return "I'm not sure how to respond to that."


@app.route("/", methods=["GET", "POST"])
def index():
    if "chat_history" not in session:
        session["chat_history"] = []

    if request.method == "POST":
        user_input = request.form["user_input"]
        ai_response = get_response(user_input)

        session["chat_history"].append(("You", user_input))
        session["chat_history"].append(("AI", ai_response))
        session.modified = True

    return render_template("index.html", chat_history=session["chat_history"])


if __name__ == "__main__":
    app.run(debug=True)
