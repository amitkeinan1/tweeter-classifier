import pandas as pd
import numpy as np
import pickle

from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.metrics import roc_auc_score
from sklearn.metrics import accuracy_score
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold

from matplotlib import pyplot as plt

stopwords = ['אני',
             'את',
             'אתה',
             'אנחנו',
             'אתן',
             'אתם',
             'הם',
             'הן',
             'היא',
             'הוא',
             'שלי',
             'שלו',
             'שלך',
             'שלה',
             'שלנו',
             'שלכם',
             'שלכן',
             'שלהם',
             'שלהן',
             'לי',
             'לו',
             'לה',
             'לנו',
             'לכם',
             'לכן',
             'להם',
             'להן',
             'אותה',
             'אותו',
             'זה',
             'זאת',
             'אלה',
             'אלו',
             'תחת',
             'מתחת',
             'מעל',
             'בין',
             'עם',
             'עד',
             'נגר',
             'על',
             'אל',
             'מול',
             'של',
             'אצל',
             'כמו',
             'אחר',
             'אותו',
             'בלי',
             'לפני',
             'אחרי',
             'מאחורי',
             'עלי',
             'עליו',
             'עליה',
             'עליך',
             'עלינו',
             'עליכם',
             'לעיכן',
             'עליהם',
             'עליהן',
             'כל',
             'כולם',
             'כולן',
             'כך',
             'ככה',
             'כזה',
             'זה',
             'זות',
             'אותי',
             'אותה',
             'אותם',
             'אותך',
             'אותו',
             'אותן',
             'אותנו',
             'ואת',
             'את',
             'אתכם',
             'אתכן',
             'איתי',
             'איתו',
             'איתך',
             'איתה',
             'איתם',
             'איתן',
             'איתנו',
             'איתכם',
             'איתכן',
             'יהיה',
             'תהיה',
             'היתי',
             'היתה',
             'היה',
             'להיות',
             'עצמי',
             'עצמו',
             'עצמה',
             'עצמם',
             'עצמן',
             'עצמנו',
             'עצמהם',
             'עצמהן',
             'מי',
             'מה',
             'איפה',
             'היכן',
             'במקום שבו',
             'אם',
             'לאן',
             'למקום שבו',
             'מקום בו',
             'איזה',
             'מהיכן',
             'איך',
             'כיצד',
             'באיזו מידה',
             'מתי',
             'בשעה ש',
             'כאשר',
             'כש',
             'למרות',
             'לפני',
             'אחרי',
             'מאיזו סיבה',
             'הסיבה שבגללה',
             'למה',
             'מדוע',
             'לאיזו תכלית',
             'כי',
             'יש',
             'אין',
             'אך',
             'מנין',
             'מאין',
             'מאיפה',
             'יכל',
             'יכלה',
             'יכלו',
             'יכול',
             'יכולה',
             'יכולים',
             'יכולות',
             'יוכלו',
             'יוכל',
             'מסוגל',
             'לא',
             'רק',
             'אולי',
             'אין',
             'לאו',
             'אי',
             'כלל',
             'נגד',
             'אם',
             'עם',
             'אל',
             'אלה',
             'אלו',
             'אף',
             'על',
             'מעל',
             'מתחת',
             'מצד',
             'בשביל',
             'לבין',
             'באמצע',
             'בתוך',
             'דרך',
             'מבעד',
             'באמצעות',
             'למעלה',
             'למטה',
             'מחוץ',
             'מן',
             'לעבר',
             'מכאן',
             'כאן',
             'הנה',
             'הרי',
             'פה',
             'שם',
             'אך',
             'ברם',
             'שוב',
             'אבל',
             'מבלי',
             'בלי',
             'מלבד',
             'רק',
             'בגלל',
             'מכיוון',
             'עד',
             'אשר',
             'ואילו',
             'למרות',
             'אס',
             'כמו',
             'כפי',
             'אז',
             'אחרי',
             'כן',
             'לכן',
             'לפיכך',
             'מאד',
             'עז',
             'מעט',
             'מעטים',
             'במידה',
             'שוב',
             'יותר',
             'מדי',
             'גם',
             'כן',
             'נו',
             'אחר',
             'אחרת',
             'אחרים',
             'אחרות',
             'אשר',
             'או']


def side_to_binary(side):
    if side == "R":
        return 1
    elif side == "L":
        return 0
    else:
        raise Exception("not such side")


def prepare_data():
    train = pd.read_excel("data//train_valid.xlsx")
    test = pd.read_excel("data//test.xlsx")

    X_train = np.array(train["texts"])
    y_train = np.array([side_to_binary(side) for side in train["sides"]])
    X_test = np.array(test["texts"])
    y_test = np.array([side_to_binary(side) for side in test["sides"]])

    return X_train, y_train, X_test, y_test


def explain_model(model, vocab):
    print('explain')
    coeffs = model.coef_[0]
    vocabs_coeffs = [(word, coeff) for word, coeff in zip(vocab, coeffs)]
    vocabs_coeffs = sorted(vocabs_coeffs, reverse=True, key=lambda x: abs(x[1]))

    for word, coeff in vocabs_coeffs[:20]:
        side = "Right" if coeff > 0 else "Left"
        print(word, side, coeff)
        print()


def explain_example(model, vocab, x, y):
    coeffs = model.coef_[0]
    vocabs_coeffs = [(word, coeff) for word, coeff in zip(vocab, coeffs)]

    word_counts = x.todense().tolist()[0]
    word_effects = [(word_coef[0], count * word_coef[1]) for count, word_coef in zip(word_counts, vocabs_coeffs)]

    word_effects = sorted(word_effects, reverse=True, key=lambda x: abs(x[1]))

    print(y)
    count = 0
    words = []
    for word, effect in word_effects:
        if (effect > 0) == y:
            words.append(word)
            count += 1
        if count == 5:
            break
    return words


def fit(X_train, y_train, X_test, y_test):
    # vector = TfidfVectorizer(max_features=500, stop_words=stopwords, ngram_range=(1, 3)).fit(X_train)
    vector = CountVectorizer(max_features=2000, stop_words=stopwords).fit(X_train)
    # pickle.dump(vector, open("pickles/countvectorizer.pkl", "wb"))
    vocab = vector.vocabulary_.keys()

    X_train_vector = vector.transform(X_train)
    X_test_vector = vector.transform(X_test)

    model = LogisticRegression(penalty="l2", C=1000)
    model.fit(X_train_vector, y_train)

    # explain_model(model, vocab)

    return X_train_vector, X_test_vector, model, vocab


def validation(X, y):
    valid_accs = []
    train_accs = []
    kf = KFold(n_splits=10)
    for train_index, test_index in kf.split(X):
        # print("TRAIN:", train_index, "TEST:", test_index)
        X_train, X_test = X[train_index], X[test_index]
        y_train, y_test = y[train_index], y[test_index]

        X_train, X_test, model, _ = fit(X_train, y_train, X_test, y_test)

        valid_preds = model.predict(X_test)
        # print(valid_preds)
        train_preds = model.predict(X_train)
        # print(train_preds[:10])

        valid_accuracy = accuracy_score(y_test, valid_preds)
        valid_accs.append(valid_accuracy)
        train_accuracy = accuracy_score(y_train, train_preds)
        train_accs.append(train_accuracy)

        # print("train accuracy:", train_accuracy)
        # print("valid accuracy:", valid_accuracy)

    print("train accuracy:", np.mean(train_accs))
    print("valid accuracy:", np.mean(valid_accs))


def test(X_train, y_train, X_test, y_test):
    X_train, X_test, model, vocab = fit(X_train, y_train, X_test, y_test)
    pickle.dump(model, open("model1.pkl", "wb"))
    pickle.dump(list(vocab), open("vocab1.pkl", "wb"))

    test_preds = model.predict(X_test)
    print(test_preds)
    pickle.dump(test_preds, open("test_predictions.pkl", "wb"))
    print(y_test)

    test_accuracy = accuracy_score(y_test, test_preds)
    print(test_accuracy)

    test_important_words = []
    for x, pred in zip(X_test, test_preds):
        important_words = explain_example(model, vocab, x, pred)
        test_important_words.append(important_words)
    pickle.dump(test_important_words, open("test_important_words.pkl", "wb"))


def play(X, y):
    valid_accs = []
    train_accs = []
    kf = KFold(n_splits=2)
    for train_index, test_index in kf.split(X):
        X_train, X_test = X[train_index], X[test_index]
        y_train, y_test = y[train_index], y[test_index]

        X_train, X_test, model, vocab = fit(X_train, y_train, X_test, y_test)

        explain_example(model, vocab, X_test[0], y_test[0])


if __name__ == '__main__':
    X_train, y_train, X_test, y_test = prepare_data()
    validation(X_train, y_train)
    # test(X_train, y_train, X_test, y_test)
