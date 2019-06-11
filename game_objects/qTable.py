import random
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

    # prev cell is the prev cell the snake was at
    # cur cell is the cell the snake moved to
    # direction is the direction the snake moved to get to cur cell
    # reward is the reward at cur cell
    def update(self, prevCell, curCell, direction, reward):
        px = prevCell[__X__]
        py = prevCell[__Y__]
        """Update current cell with new Q value"""
        self.table[px * py][direction] = (1 - self.learnRate) * self.table[px * py][direction] + self.learnRate * (reward + self.discountRate * self.nextAction(curCell))

    def nextAction(self, curCell):
        if curCell is None:
            return 0
        else:
            cx = curCell[__X__]
            cy = curCell[__Y__]
            return max(self.table[cx * cy])

    """coordinate is a list of X and Y located at head of snake"""
    # Can possibly take the discountRate comparison out for testing purposes
    def getMax(self, coordinate):
        maxDir = None
        curState = self.table[coordinate[__X__] * coordinate[__Y__]]
        """if all state elements are equal or we choose to go in random direction"""
        if random.random() < self.discountRate or np.array_equal(curState, curState):
            maxDir = random.randint(0, 3)
        else:
            curState = np.tolist(curState)
            """gets the max qtable value from all possible directions for deciding which direction to go"""
            maxDir = curState.index(max(curState))
        """direction corosponding to the direction enum"""
        return maxDir
