import numpy as np
from math import exp
import numba

from numpy.lib.function_base import _parse_input_dimensions


@numba.njit
def sigmoid(x: float) -> float:
    return 1 / (1 + exp(-x))


@numba.njit
def deriviatesigmoid(y):
    # return sigmoid(x) *(1 -sigmoid(x))
    return y * (1-y)


class NeuralNetwork:
    def __init__(self, Numberinput, Numberhidden, Numberoutput):
        self.Inputnodes = Numberinput
        self.Hiddennodes = Numberhidden
        self.OutputNodes = Numberoutput
        # Skapar vikter för de oliak lagrerna och ger dem random värden.
        self.weights_ih = np.random.uniform(
            low=-1, high=1, size=(self.Hiddennodes, self.Inputnodes))
        self.weights_ho = np.random.uniform(
            low=-1, high=1, size=(self.OutputNodes, self.Hiddennodes))

        # Skapar bias för de oliak lagrerna och ger dem random värden.

        self.bias_h = np.random.uniform(
            low=-1, high=1, size=(self.Hiddennodes, 1))
        self.bias_o = np.random.uniform(
            low=-1, high=1, size=(self.OutputNodes, 1))
        self.learningrate = 0.1

    # Det som skickas frammåt
    def feedforward(self, input_array):
        # Ta in värden i form av array, gör om dem till en endimensionell Matrix.
        inputs = np.array([input_array]).T
        # Skapar en ny matrix från värdena och vikterna.
        hidden = self.weights_ih.dot(inputs)

        # Lägger till Biasen
        hidden += self.bias_h
        # Kör Aktiveringsmetoden (sigmoid i detta fall)
        hidden = np.vectorize(sigmoid)(hidden)
        # Gör samma en gång till fast för output layern
        output = self.weights_ho.dot(hidden)
        output += self.bias_o
        output = np.vectorize(sigmoid)(output)
        # Gör om det till en array och returnerar det.
        return output.flatten()

    def train(self, input_array, target_array):
        # Ta in värden i form av array, gör om dem till en endimensionell Matrix.
        inputs = np.array([input_array]).T
        # Skapar en ny matrix från värdena och vikterna.
        # Lägger till Biasen
        hidden = self.weights_ih.dot(inputs) + self.bias_h
        # Kör Aktiveringsmetoden (sigmoid i detta fall)
        hidden = np.vectorize(sigmoid)(hidden)

        # Gör samma en gång till fast för output layern
        outputs = self.weights_ho.dot(hidden) + self.bias_o
        # Kör Aktiveringsmetoden (sigmoid i detta fall)
        outputs = np.vectorize(sigmoid)(outputs)


        targets = np.array([target_array]).T

        # Räknar ut error, error = targets - outputs
        output_errors = targets - outputs
        hidden_errors = (self.weights_ho.T).dot(output_errors)

        #   gradient = outputs * (1-outputs)
        # Räknar ut gradient
        gradients = np.vectorize(deriviatesigmoid)(outputs)
        gradients = self.learningrate * np.multiply(gradients, output_errors)

        # Räknar ut deltas
        weights_ho_deltas = gradients.dot(hidden.T)

        # Justera vikterna efter dess deltas
        self.weights_ho += weights_ho_deltas
        # Justera bias efter dess deltas (gradients)
        self.bias_o += gradients


        # Räknar ut erroret på hidden layer
        
        hidden_gradient = np.vectorize(deriviatesigmoid)(hidden)
        hidden_gradient = self.learningrate * np.multiply(hidden_gradient, hidden_errors)

        # Räknar ut hidden deltas
        weights_ih_deltas = hidden_gradient.dot(inputs.T)

        # Justera vikterna efter dess deltas
        self.weights_ih += weights_ih_deltas
        # Justera bias efter dess deltas (gradients)
        self.bias_h += hidden_gradient

        # outputs.print()
        # targets.print()
        # output_errors.print()

        # hidden_errors.print()


