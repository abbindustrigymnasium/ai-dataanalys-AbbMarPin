import numpy as np
from sklearn import preprocessing, neighbors, model_selection
import pandas as pd

print("Laddar csv")
df = pd.read_csv("votering.csv")
print("klar")

df.drop(["punkt"], 1, inplace=True)

df = df[["rost", "parti", "fodd", "kon", "intressent_id"]]
print(df.head(3))
inputLabel = ["kvinna", "man"]
encoder = preprocessing.LabelEncoder()
encoder.fit(inputLabel)
df["kon"] = encoder.transform(df["kon"])

inputLabel = ["C", "KD", "M", "L", "MP", "V", "S", "SD", "-"]
encoder.fit(inputLabel)
df["parti"] = encoder.transform(df["parti"])


inputLabel = ["Ja", "Nej", "Frånvarande"]
encoder.fit(inputLabel)
df["parti"] = encoder.transform(df["parti"])


for i, item in enumerate(encoder.classes_):
    print(item, "\t--->", i)
