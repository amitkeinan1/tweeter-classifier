from get_tweets import get_tweets_of_user
from parse_texts import get_one_text
from model import explain_example
import pickle
import os
import json


def predict_by_model(user, model, vectorizer, vocab):
    tweets = get_tweets_of_user(user)
    text = get_one_text(tweets)
    x = vectorizer.transform([text])
    pred = model.predict(x)[0]

    important_words = explain_example(model, vocab, x, pred)

    return pred, important_words


def predict_user(user, model_name):
    pred, words, found = check_cache(user, model_name)
    print(found)
    if not found:
        model = pickle.load(open(f"pickles//{model_name}//model.pkl", "rb"))
        count_vectorizer = pickle.load(open(f"pickles//{model_name}//countvectorizer.pkl", "rb"))
        vocab = pickle.load(open(f"pickles//{model_name}//vocab.pkl", "rb"))
        pred, words = predict_by_model(user, model, count_vectorizer, vocab)
        save_prediction(user, str(pred), words, model_name)
        pred = str(pred)

    prediction_dict = {'0': "Leftist", '1': "Rightist"}

    return prediction_dict[pred], words


def check_cache(user, model_name):
    file_name = f"cache/{model_name}/{user}.json"
    if os.path.isfile(file_name):
        data = json.loads(open(file_name, "r", encoding="utf8").read())
        return data["prediction"], data["words"], True
    else:
        return -1, - 1, False


def save_prediction(user, prediction, words, model_name):
    file_name = f"cache/{model_name}/{user}.json"
    data = {"prediction": prediction, "words": words}
    with open(file_name, 'w+', encoding="utf8") as f:
        json.dump(data, f)


if __name__ == '__main__':
    user = "meir_amrani"
    model_name = "2-all"
    pred, words = predict_user(user, model_name)
    print(pred)
    print(words)
