import pandas as pd
import re
import string
import os


def read_text_file(file_name):
    with open(file_name, 'r', encoding="utf8") as my_file:
        lines = my_file.readlines()
    lines = [line.strip() for line in lines]
    return lines


def get_texts_from_excel(file_name):
    texts = pd.read_excel(file_name)
    return list(texts["tweets"])


def remove_html(text):
    html = re.compile(r'<.*?>')
    return html.sub(r'', text)


def remove_punct(text):
    table = str.maketrans('', '', string.punctuation)
    return text.translate(table)


def remove_urls(text):
    text = re.sub(r"http\S+", "", text)
    return text


def remove_emoji(text):
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               u"\U00002702-\U000027B0"
                               u"\U000024C2-\U0001F251"
                               "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', text)


def concat_texts(texts):
    return ' '.join(texts)


def clean_text(text):
    text = remove_urls(text)
    text = remove_html(text)
    text = remove_punct(text)
    text = remove_emoji(text)
    text = text.replace("\n", " ")
    text = text.replace("RT ", "")
    return text


def get_one_text(texts):
    cleaned_texts = [clean_text(text) for text in texts]
    concat_text = concat_texts(cleaned_texts)
    return concat_text


def get_one_text_from_excel(user, side):
    texts = get_texts_from_excel(f"tweets\\{side}\\{user}.xlsx")
    concat_text = get_one_text(texts)


if __name__ == '__main__':
    right_users = [file[:-5] for file in os.listdir("tweets//right")]
    left_users = [file[:-5] for file in os.listdir("tweets//left")]

    users = []
    sides = []
    texts = []

    for user in right_users:
        text = get_one_text_from_excel(user, "right")
        users.append(user)
        sides.append("R")
        texts.append(text)

    for user in left_users:
        text = get_one_text_from_excel(user, "left")
        users.append(user)
        sides.append("L")
        texts.append(text)

    df = pd.DataFrame({"users": users, "sides": sides, "texts": texts})

    df.to_excel("data//all_data.xlsx")
