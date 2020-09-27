from get_tweets import get_tweets_of_user
from parse_texts import get_one_text
import pickle
import os
import logging
logging.getLogger().addHandler(logging.StreamHandler())


def predict_user(user):
    pred, found = check_cache(user)
    logging.info(f"user {user} found in cache? {found}")
    if not found:
        tweets = get_tweets_of_user(user)
        text = get_one_text(tweets)
        count_vectorizer = pickle.load(open("pickles/countvectorizer1.pkl", "rb"))
        model = pickle.load(open("pickles/model1.pkl", "rb"))
        x = count_vectorizer.transform([text])
        pred = model.predict(x)[0]
        save_prediction(user, str(pred))

    if pred == 0:
        return "Leftist"
    elif pred == 1:
        return "Rightist"
    else:
        raise Exception("problem")


def check_cache(user):
    file_name = f"cache/model1/{user}.txt"
    if os.path.isfile(file_name):
        with open(file_name, 'r') as file:
            prediction = file.read()
            return int(prediction), True
    else:
        return -1, False


def save_prediction(user, prediction):
    with open(f"cache/model1/{user}.txt", 'w+') as file:
        file.write(prediction)


if __name__ == '__main__':
    user = "yoav8941849118914117489719198r"
    pred = predict_user(user)
    print(pred)
