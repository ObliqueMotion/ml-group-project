import math
import torch
import torch.nn as nn
from game_objects.direction import Direction

__UP__    = 0
__DOWN__  = 1
__LEFT__  = 2
__RIGHT__ = 3

def intercalate(lst, item):
    """Inserts an item between each element of a list"""
    result = [item] * (len(lst) * 2 - 1)
    result[0::2] = lst
    return result

class DirectionNet:
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
            layers.append(nn.Sigmoid())
            self.network = nn.Sequential(*layers)
            self.criterion = nn.MSELoss()
            self.optimizer = torch.optim.SGD(self.network.parameters(), lr=lr)


    def eval(self, input):
        """Evaluates the input of a network, outputing some confidence in range [-1.0, 1.0]"""
        self.output = self.network(input)
        return float(self.output)

    def update(self, target):
        """Updates the weights based on a provided target in range [-1.0, 1.0]"""
        self.loss = self.criterion(self.output, target)
        self.optimizer.zero_grad()
        self.loss.backward()
        self.optimizer.step()
            


class SplitBrainNetwork:
    up_nn = None
    down_nn = None
    left_nn = None
    right_nn = None
    direction = None
    outputs = None

    def __init__(self, **kwargs):
        """Initializes a new network with 4 sub-networks for each direction"""
        if "dimensions" in kwargs and "lr" in kwargs:
            lr = kwargs.pop("lr", False)
            dimensions = kwargs.pop("dimensions", False)
            self.up_nn    = DirectionNet(dimensions=dimensions, lr=lr)
            self.down_nn  = DirectionNet(dimensions=dimensions, lr=lr)
            self.left_nn  = DirectionNet(dimensions=dimensions, lr=lr)
            self.right_nn = DirectionNet(dimensions=dimensions, lr=lr)
        
    def eval(self, inputs):
        """Evaluates a set of inputs returning a new Direction for the snake to travel"""
        self.outputs = [
            self.up_nn.eval(inputs[__UP__]),
            self.down_nn.eval(inputs[__DOWN__]),
            self.left_nn.eval(inputs[__LEFT__]),
            self.right_nn.eval(inputs[__RIGHT__])
        ]

        if math.isclose(max(self.outputs), self.outputs[__UP__], rel_tol=1e-9):
            self.direction = Direction.up
        if math.isclose(max(self.outputs), self.outputs[__DOWN__], rel_tol=1e-9):
            self.direction = Direction.down
        if math.isclose(max(self.outputs), self.outputs[__LEFT__], rel_tol=1e-9):
            self.direction = Direction.left
        if math.isclose(max(self.outputs), self.outputs[__RIGHT__], rel_tol=1e-9):
            self.direction = Direction.right

        return self.direction

    def update(self, target):
        """Updates the weights of the relevant sub-network based on the target and the current direction."""
        if self.direction is Direction.up:
            self.up_nn.update(target)
        if self.direction is Direction.down:
            self.down_nn.update(target)
        if self.direction is Direction.left:
            self.left_nn.update(target)
        if self.direction is Direction.right:
            self.right_nn.update(target)

    def display_outputs(self):
        """Displays the outputs of each subnetwork to the console."""
        print(
            "Up: (", str(round(self.outputs[__UP__], 3)), ")",
            "    \tDown: (", str(round(self.outputs[__DOWN__], 3)), ")",
            "    \tLeft: (", str(round(self.outputs[__LEFT__], 3)), ")",
            "    \tRight: (", str(round(self.outputs[__RIGHT__], 3)), ")"
        )