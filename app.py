from flask import Flask, render_template, request
from chatbot import predict_class, get_response, name_replace, intents
from builtins import zip

app = Flask(__name__)
app.config["SECRET_KEY"] = "a_secret_ket_12345"

response_list = []
quest_resp = []

@app.route("/")
def home():
    global response_list
    response_list.clear()
    return render_template("index.html")

@app.route("/chatbot", methods=["GET", "POST"])
def chatbot():
    global response_list
    global quest_resp
    if request.method == "POST":
        quest_resp.clear()
        message = request.form["message"]
        quest_resp.append(message)   # needed to show user input?
        ints = predict_class(message.lower())
        res = get_response(ints, intents)
        res = name_replace(res)
        quest_resp.append(res)
        response_list.append(quest_resp[:])
        if len(response_list) > 4:
            del response_list[0]
        return render_template("chatbot.html", message=message, response_list=response_list)
    return render_template("chatbot.html", message="", response_list=response_list)

if __name__ == "__main__":
    app.run(debug=True)

