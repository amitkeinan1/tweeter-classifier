from flask import Flask, render_template
import os

from predict import predict_user

app = Flask(__name__)

MODEL_NAME = "2-all"
ERROR_MSG = "משהו לא עבד כאן... וודא שהזנת שם נכון, כמו שמופיע אחרי ה-@"


@app.route('/')
def hello():
    return render_template("home.html")


@app.route('/<user>', methods=['GET'])
def check_in(user):
    try:
        pred, words = predict_user(user, MODEL_NAME)
        return render_template("result.html", user=user, pred=pred, words=words)
    except Exception:
        return render_template("error.html")


if __name__ == '__main__':
    app.run()
