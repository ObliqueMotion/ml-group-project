import math
import torch
import torch.nn as nn

def intercalate(lst, item):
    """Inserts an item between each element of a list"""
    result = [item] * (len(lst) * 2 - 1)
    result[0::2] = lst
    return result

class DQN:
    loss = None
    output = None
    network = None
    criterion = None
    optimizer = None

    # example: if dimensions = [4, 100, 50, 1] this will create
    # a neural network with 4 inputs, 100 units in the first hidden layer,
    # 50 units in the second hidden layer, and 1 output.
    def __init__(self, **kwargs):
        """Initializes a DirectionNet"""
        if "dimensions" in kwargs and "lr" in kwargs:
            lr = kwargs.pop("lr", False)
            dimensions = kwargs.pop("dimensions", False)
            pairs = list(zip(dimensions, dimensions[1:]))
            layers = list(map(lambda pair: nn.Linear(pair[0], pair[1]), pairs))
            layers = intercalate(layers, nn.LeakyReLU(0.1))
            layers.append(nn.Tanh())
            self.network = nn.Sequential(*layers)
            self.criterion = nn.MSELoss()
            self.optimizer = torch.optim.SGD(self.network.parameters(), lr=lr)


    def eval(self, input):
        """Evaluates the input of a network, outputing some confidence in range [-1.0, 1.0]"""
        self.output = self.network(input)
        return self.output

    def update(self, target):
        """Updates the weights based on a provided target in range [-1.0, 1.0]"""
        self.loss = self.criterion(self.output, target)
        self.optimizer.zero_grad()  # look this up later
        self.loss.backward()
        self.optimizer.step()

