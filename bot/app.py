from flask import Flask, render_template, jsonify, request
from response import getRespons

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("base.html")

@app.route("/send_message", methods=['POST'])
def send_message():
    text = request.form["message"]
    print(text)
    response = getRespons(text)
    message = {"answer": response}
    print(message)
    return jsonify(message)

if __name__ =="__main__":
    app.run(debug=True)
    