import random
import torch
from game_objects.direction import Direction

__X__ = 0
__Y__ = 1


class qTable():
    table = None
    learnRate = None
    discountRate = None

    def __init__(self, length, height, learnRate, discountRate):
        self.table = torch.zeros((length, height, 4))
        torch.set_printoptions(threshold=length*height*4, profile="full")
        self.learnRate = learnRate
        self.discountRate = discountRate

    # prev cell is the prev cell the snake was at
    # cur cell is the cell the snake moved to
    # direction is the direction the snake moved to get to cur cell
    # reward is the reward at cur cell
    def update(self, prevCell, curCell, direction, reward):
        px = prevCell[__X__]
        py = prevCell[__Y__]
        # Update current cell with new Q value
        self.table[px][py][direction] = self.table[px][py][direction] + self.learnRate * (reward + self.discountRate * self.nextAction(curCell) - self.table[px][py][direction])
        # print(self.table[px][py][direction])

    def Print(self):
        print(self.table)
        
    def nextAction(self, curCell):
        if curCell is None:
            return 0
        else:
            cx = curCell[__X__]
            cy = curCell[__Y__]
        # DELETE COMMENT LATER: want to see all directions?
            return max(self.table[cx][cy][:])

    """coordinate is a list of X and Y located at head of snake"""
    # Can possibly take the discountRate comparison out for testing purposes
    def getMax(self, coordinate, direction):
        maxDir = None
        curState = self.table[coordinate[__X__]][coordinate[__Y__]][:]
        # if all state elements are equal or we choose to go in random direction
        # random.random() < self.discountRate or
        if curState[0] == curState[1] and curState[0] == curState[2] and curState[0] == curState[3]:
            maxDir = random.randint(0, 3)
            if maxDir == 0 and direction == 1:
                maxDir = random.sample([1, 2, 3], 1)[0]
            elif maxDir == 1 and direction == 0:
                maxDir = random.sample([0, 2, 3], 1)[0]
            elif maxDir == 2 and direction == 3:
                maxDir = random.sample([0, 1, 3], 1)[0]
            elif maxDir == 3 and direction == 2:
                maxDir = random.sample([0, 1, 2], 1)[0]
        else:
            curState = curState.tolist()
            # gets the max qtable value from all possible directions for deciding which direction to go
            maxDir = curState.index(max(curState))
            if maxDir == 0 and direction == 1:
                maxDir = curState.index(sorted(curState)[-2])
            elif maxDir == 1 and direction == 0:
                maxDir = curState.index(sorted(curState)[-2])
            elif maxDir == 2 and direction == 3:
                maxDir = curState.index(sorted(curState)[-2])
            elif maxDir == 3 and direction == 2:
                maxDir = curState.index(sorted(curState)[-2])
        # direction corresponding to the direction enum
        return Direction(maxDir)
