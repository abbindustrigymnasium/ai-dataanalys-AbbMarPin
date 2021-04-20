import Neural
import random
from tqdm import trange

trainingdata = [
    {"inputs": [0, 1], "targets": [1]},
    {"inputs": [0, 0], "targets": [0]},
    {"inputs": [1, 0], "targets": [1]},
    {"inputs": [1, 1], "targets": [0]}
]
testingdata = [
    [0, 0], [0, 1], [1, 0], [1, 1]
]
# Skapar nätverket
nn = Neural.NeuralNetwork(2, 5, 1)

# Skapar tränar det 100000 gånger
for i in trange(100000):
    data = random.choice(trainingdata)
    nn.train(data["inputs"], data["targets"])
# Testar det med testdatavärdena vi har angett ovan
print()
for test in testingdata:
    answer = nn.feedforward(test)
    print(test, answer)


# answer = nn.feedforward(testingdata[0])
# print(testingdata[0], answer)
