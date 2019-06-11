import math
import torch
import random
import torch.nn as nn

def intercalate(lst, item):
    """Inserts an item between each element of a list"""
    result = [item] * (len(lst) * 2 - 1)
    result[0::2] = lst
    return result

class DQN:
    loss = None
    output = None
    outputs = None
    targets = None
    network = None
    criterion = None
    optimizer = None
    batch_size = None
    sample_size = None
    state_count = None

    # example: if dimensions = [4, 100, 50, 1] this will create
    # a neural network with 4 inputs, 100 units in the first hidden layer,
    # 50 units in the second hidden layer, and 1 output.
    def __init__(self, **kwargs):
        """Initializes a DirectionNet"""
        if "dimensions" in kwargs and "lr" in kwargs and "batch_size" in kwargs and "sample_size" in kwargs:
            lr = kwargs.pop("lr", False)
            dimensions = kwargs.pop("dimensions", False)
            self.batch_size = kwargs.pop("batch_size", False)
            self.sample_size = kwargs.pop("sample_size", False)
            pairs = list(zip(dimensions, dimensions[1:]))
            layers = list(map(lambda pair: nn.Linear(pair[0], pair[1]), pairs))
            layers = intercalate(layers, nn.LeakyReLU(0.1))
            layers.append(nn.Tanh())
            self.network = nn.Sequential(*layers)
            self.criterion = nn.MSELoss()
            self.optimizer = torch.optim.SGD(self.network.parameters(), lr=lr)
            self.inputs = []
            self.targets = []
            self.state_count = 0


    def eval(self, inputs):
        """Evaluates the input of a network, outputing some confidence in range [-1.0, 1.0] for each direction (up, down, left, right)"""
        self.output = self.network(inputs)
        return self.output

    def add_to_replay_memory(self, inputs, targets):
        """Ands an (input-state, reward) pair to the replay memory that may be used for training."""
        self.state_count += 1
        self.inputs.append(inputs)
        self.targets.append(targets)

    def update(self):
        """Choses random samples from the replay memory and updates the weights according to the sample."""
        if self.state_count >= self.batch_size:
            for (inputs, targets) in random.sample(list(zip(self.inputs, self.targets)), self.sample_size):
                output = self.network(inputs)
                loss = self.criterion(output, targets)
                self.optimizer.zero_grad()
                loss.backward()
                self.optimizer.step()
            self.inputs = []
            self.targets = []
            self.state_count = 0