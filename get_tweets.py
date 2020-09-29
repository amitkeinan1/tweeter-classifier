import twitter
import pandas as pd
import os
import concurrent.futures
import logging

consumer_key = "Y10IclmXbqLuyaEsfBxOEB1TF"
consumer_secret = "NKSv6MEcJVuj47VMfzjTfxl4IqYJBUeJupV1rCtnkywW3jvVFu"
access_token = "964906800389808128-dQMU1SqETThRJ0pd9bxTb0f0DDVtRnk"
access_token_secret = "l4tJlvblYkmqUWO9atrLADHNZqeYpRGixZPRHgCmFlRWS"


def get_tweets_of_user(user):
    api = twitter.Api(consumer_key=consumer_key,
                      consumer_secret=consumer_secret,
                      access_token_key=access_token,
                      access_token_secret=access_token_secret)
    logging.warning(user)
    tweets = api.GetUserTimeline(screen_name="amit_segal", count=200)
    texts = [tweet.text for tweet in tweets]
    return texts


def save_texts_in_file(file_name, texts):
    tweets_df = pd.DataFrame({"tweets": texts})
    tweets_df.to_excel(file_name)


def read_text_file(file_name):
    with open(file_name, 'r', encoding="utf8") as my_file:
        lines = my_file.readlines()
    lines = [line.strip() for line in lines]
    return lines


def save_user_tweets(user, side):
    if not os.path.isfile(f"tweets\\{side}\\{user}.xlsx"):
        print(user)
        texts = get_tweets_of_user(user)
        print(len(texts))
        save_texts_in_file(f"tweets\\{side}\\{user}.xlsx", texts)


if __name__ == '__main__':
    right_users = read_text_file("users//right.txt")
    left_users = read_text_file("users//left.txt")

    executor = concurrent.futures.ProcessPoolExecutor(20)
    futures = [executor.submit(save_user_tweets, user, "right") for user in right_users]
    concurrent.futures.wait(futures)

