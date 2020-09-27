from flask import Flask

from predict import predict_user

app = Flask(__name__)

message = "The site will be redployed after YOM KIPUR. gmar hatima tova!"


@app.route('/')
def hello():
    return message


@app.route('/<user>', methods=['GET'])
def check_in(user):
    return message


if __name__ == '__main__':
    app.run()
