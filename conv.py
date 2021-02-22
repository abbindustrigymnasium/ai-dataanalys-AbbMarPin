import pandas as pd

offset = 100

data = pd.read_csv("cykel.txt", sep=";")

data["time[s]"] = data["pulses"] * 1/50
data["time[s]_mov"] = offset + (data["pulses"] * 1/50)


print(data)