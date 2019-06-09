import numpy as np

__X__ = 0
__Y__ = 1


class qTable():
    table = None
    learnRate = None
    discountRate = None

    def __init__(self, length, height, learnRate, discountRate):
        self.table = np.zeros((length * height, 4))
        self.learnRate = learnRate
        self.discountRate = discountRate

    def update(self, prevCell, curCell, direction, reward):
        px = prevCell[__X__]
        py = prevCell[__Y__]
        cx = curCell[__X__]
        cy = curCell[__Y__]
        """Update current cell with new Q value"""
        self.table[px * py][direction] = (self.table[px * py][direction] +
                                          self.learnRate * (reward + self.discountRate *
                                          np.max(self.table[cx * cy]) -
                                          self.table[px * py][direction]))

    """coordinate is a list of X and Y located at head of snake"""
    def getMax(self, coordinate):
        adjSpaces = self.table[coordinate[__X__] * coordinate[__Y__]]
        adjSpaces = np.tolist(adjSpaces)
        """gets the max qtable value from all possible directions for deciding which direction to go"""
        maxDir = adjSpaces.index(max(adjSpaces))
        """direction corosponding to the direction enum"""
        return maxDir
