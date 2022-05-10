import numpy as np


class ValueContainer:
    def __init__(self, value):
        self.value = value


class NeuralNetwork:
    def __init__(self, input_size, output_size):
        self.weights = np.random.rand(input_size, output_size) - 0.5
        self.bias = np.random.rand(1, output_size) - 0.5


class Link(ValueContainer):
    def __init__(self, value):
        super().__init__(value)


class Node(ValueContainer):
    def __init__(self, value):
        super().__init__(value)


class InNode(ValueContainer):
    def __init__(self, value):
        super().__init__(value)


class OutNode(ValueContainer):
    def __init__(self, value):
        super().__init__(value)
