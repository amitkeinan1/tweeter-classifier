import pandas as pd
from sklearn.model_selection import train_test_split


df = pd.read_excel("data//all_data.xlsx")


train_valid, test = train_test_split(df, test_size=0.1)
train_valid.to_excel("data//train_valid.xlsx")

train, valid = train_test_split(train_valid, test_size=0.15)

train.to_excel("data//train.xlsx")
valid.to_excel("data//valid.xlsx")
test.to_excel("data//test.xlsx")

