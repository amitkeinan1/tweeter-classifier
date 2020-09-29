from flask import Flask, render_template, request, redirect
import os

from predict import predict_user

app = Flask(__name__)

MODEL_NAME = "2-all"
ERROR_MSG = "משהו לא עבד כאן... וודא שהזנת שם נכון, כמו שמופיע אחרי ה-@"


@app.route('/')
def home():
    return render_template("home.html")


@app.route('/', methods=['POST'])
def my_form_post():
    user = request.form['user']
    return redirect(f"/{user}")


@app.route('/<user>', methods=['GET'])
def predict_user_site(user):
    try:
        pred, words = predict_user(user, MODEL_NAME)
        return render_template("result.html", user=user, pred=pred, words=words)
    except Exception:
        return render_template("error.html")


if __name__ == '__main__':
    app.run()
