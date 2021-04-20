import random
import tqdm
from numba import jit

class Trainer:
    def __init__(self, x, y, a):
        self.inputs = [x, y, 1]
        self.answer = a


class Perceptron:
    def __init__(self, weights):
        self.weights = [random.random()*2-1 for _ in range(weights)]
        self.lr = 0.00001

    def train(self, inputs: list, desired: int) -> None:
        # Guess the result
        guess = self.feedforward(inputs)
        # Compute the factor for changing the weight based on the error
        # Error = desired output - guessed output
        # Note this can only be 0, -2, or 2
        # Multiply by learning constant
        error = desired - guess
        # Adjust weights based on weightChange * input
        for i, inp in enumerate(inputs):
            self.weights[i] += self.lr * error * inp

    def feedforward(self, inputs: list):
        s = 0.0
        for inp, weight in zip(inputs, self.weights):
            s += inp*weight

        # Result is sign of the s, -1 or 1
        return activate(s)

# @jit(nopython=True)
def activate(s: float) -> int:
    if (s > 0):
        return 1
    else:
        return -1

xmin = -300
ymin = -300
xmax =  300
ymax =  300

# The function to describe a line 
def f(x):
  return 0.4*x+1


# ptron = Perceptron(3)

# training = []

# for i in tqdm.trange(1000000):
#     x = random.randint(xmin, xmax)
#     y = random.randint(ymin, ymax)
#     answer = 1
#     if (y < f(x)):
#         answer = -1
#     training.append(Trainer(x, y, answer))

# for x in tqdm.tqdm(training):
#     ptron.train(x.inputs, x.answer)

# print(ptron.weights)



