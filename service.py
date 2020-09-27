from flask import Flask

from predict import predict_user

app = Flask(__name__)


@app.route('/')
def hello():
    return 'Hello!'


@app.route('/<user>', methods=['GET'])
def check_in(user):
    return predict_user(user)


if __name__ == '__main__':
    app.run()
