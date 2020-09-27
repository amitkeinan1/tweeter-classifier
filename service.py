from flask import Flask
import logging

from predict import predict_user

app = Flask(__name__)


@app.route('/')
def hello():
    return 'Hello!'


@app.route('/<user>', methods=['GET'])
def check_in(user):
    logging.INFO(f"got request for {user}")
    prediction = predict_user(user)
    logging.INFO(f"prediction: user {user} is {prediction}")
    return prediction


if __name__ == '__main__':
    app.run()
