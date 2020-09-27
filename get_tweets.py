import twitter
import pandas as pd

consumer_key = "Y10IclmXbqLuyaEsfBxOEB1TF"
consumer_secret = "NKSv6MEcJVuj47VMfzjTfxl4IqYJBUeJupV1rCtnkywW3jvVFu"
access_token = "964906800389808128-M5ixJPuZKWVjFh27gZKwTQnWLMKA2zH"
access_token_secret = "9Cg9y63LII3gy4uYM8hF95VhK6sX26vBV1YY1IBUS8FYv"


def get_tweets_of_user(user):
    api = twitter.Api(consumer_key=consumer_key,
                      consumer_secret=consumer_secret,
                      access_token_key=access_token,
                      access_token_secret=access_token_secret)
    tweets = api.GetUserTimeline(screen_name=user, count=200)
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


if __name__ == '__main__':
    right_users = read_text_file("right.txt")
    left_users = read_text_file("left.txt")

    print("right")
    for user in right_users:
        print(user)
        texts = get_tweets_of_user(user)
        print(len(texts))
        save_texts_in_file(f"tweets\\right\{user}.xlsx", texts)
        print()

    print("left")
    for user in left_users:
        print(user)
        texts = get_tweets_of_user(user)
        print(len(texts))
        save_texts_in_file(f"tweets\\left\{user}.xlsx", texts)
        print()