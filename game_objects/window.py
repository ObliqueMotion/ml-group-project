import matplotlib
import matplotlib.pyplot as plt
import math
import torch
import copy
import pygame as pg
from pygame.locals import *
from pygame.color import Color
from models.split_brain import SplitBrainNetwork
from game_objects.grid import Grid
from game_objects.cell import CellType
from game_objects.direction import Direction
from game_objects.qTable import qTable
from models.DQN import DQN
from game_objects.reward import reward

__SNAKE_CELL_PATH__ = "images/white_square.png"
__APPLE_CELL_PATH__ = "images/green_square.png"

__UP__ = 0
__DOWN__ = 1
__LEFT__ = 2
__RIGHT__ = 3


# The GameWindow is responsible for running the main game loop.
# The GameWindow is responsible for drawing the game state to the screen.
class GameWindow:
    dqn = None
    grid = None
    clock = None
    score = None
    scores = None
    height = None
    length = None
    avrages = None
    actions = None
    surface = None
    cell_size = None
    is_training = None
    training_pressed = None
    actions_per_second = None
    split_brain_network = None
    num = None

    def __init__(self, **kwargs):
        """Initializes the game window."""
        pg.init()
        pg.display.set_caption('Snake')
        self.clock = pg.time.Clock()
        if 'cell_size' in kwargs:
            self.cell_size = kwargs.pop('cell_size', False)
        if 'length' in kwargs:
            self.length = kwargs.pop('length', False)
        if 'height' in kwargs:
            self.height = kwargs.pop('height', False)
        if 'speed' in kwargs:
            self.actions_per_second = kwargs.pop('speed', False)
        self._exit = False
        self.is_training = True
        self.trainig_pressed = False
        self.score = 0
        self.actions = 0
        self.scores = []
        self.averages = []

        # For split-brain network
        if "sb_dimensions" and "sb_lr" in kwargs:
            dimensions = kwargs.pop("sb_dimensions", False)
            lr = kwargs.pop("sb_lr", False)
            self.split_brain_network = SplitBrainNetwork(dimensions=dimensions, lr=lr)

        # DQN
        if "dqn_dimensions" and "dqn_lr" and "dqn_batch_size" and "dqn_sample_size" in kwargs:
            dimensions = kwargs.pop("dqn_dimensions", False)
            lr = kwargs.pop("dqn_lr", False)
            batch_size = kwargs.pop("dqn_batch_size", False)
            sample_size = kwargs.pop("dqn_sample_size", False)
            self.dqn = DQN(dimensions=dimensions, lr=lr, batch_size=batch_size, sample_size=sample_size)

    def plot_scores(self):
        plt.figure(2)
        plt.clf()
        plt.title('Training...')
        plt.xlabel('Games')
        plt.ylabel('Score')
        plt.plot(self.scores)
        plt.plot(self.averages)
        plt.pause(0.001)  # pause a bit so that plots are update

        self.agent = qTable(self.length, self.height, 0.5, 0.8)

    def reset(self, **kwargs):
        """Resets the game state with a new snake and apple in random positions."""
        pg.display.set_caption('Snake')

        self._surface = pg.display.set_mode(
            (self.length * self.cell_size, self.height * self.cell_size),
            pg.HWSURFACE
        )
        self.grid = Grid(
            cell_size=self.cell_size,
            length=self.length,
            height=self.height
        )
        self.snake_cell_image = pg.image.load(__SNAKE_CELL_PATH__).convert()
        self.snake_cell_image = pg.transform.scale(
            self.snake_cell_image,
            (self.cell_size, self.cell_size)
        ).convert()

        self.apple_cell_image = pg.image.load(
            __APPLE_CELL_PATH__
        ).convert()

        self.apple_cell_image = pg.transform.scale(
            self.apple_cell_image, (self.cell_size, self.cell_size)).convert_alpha()

        self.score = 0
        self.actions = 0
        self._exit = False

    def check_for_exit(self):
        """Checks if the user has decided to exit."""
        keys = pg.key.get_pressed()
        if (keys[K_ESCAPE]):
            self._exit = True
        for event in pg.event.get():
            if event.type == QUIT:
                self._exit = True

    def handle_keyboard_input(self):
        """Checks for input to the game."""
        keys = pg.key.get_pressed()

        if (keys[K_UP]):
            self.grid.change_direction(Direction.up)
        if (keys[K_DOWN]):
            self.grid.change_direction(Direction.down)
        if (keys[K_LEFT]):
            self.grid.change_direction(Direction.left)
        if (keys[K_RIGHT]):
            self.grid.change_direction(Direction.right)
        if (keys[K_SPACE]):
            self.grid.snake.grow()
        if (keys[K_RIGHTBRACKET]):
            self.actions_per_second += 1
        if (keys[K_LEFTBRACKET]):
            self.actions_per_second -= 1
        if (keys[K_t]):
            self.is_training = True
            print("========================================================================")
            print("Training: ON")
            print("========================================================================")
        if (keys[K_s]):
            self.is_training = False
            print("========================================================================")
            print("Training: OFF")
            print("========================================================================")

    def perform_keyboard_actions(self):
        """Executes all relevant game-state changes."""
        self.handle_keyboard_input()
        self.grid.next_frame()

    def perform_DQN_actions(self):
        proximity = self.grid.proximity_to_apple()
        safety_limit = 0.5
        inputs = torch.tensor([
            proximity,
            self.grid.safe_cells_up_global(),
            self.grid.safe_cells_up(),
            self.grid.apple_is_up_safe(safety_limit),
            self.grid.safe_cells_down_global(),
            self.grid.safe_cells_down(),
            self.grid.apple_is_down_safe(safety_limit),
            self.grid.safe_cells_left_global(),
            self.grid.safe_cells_left(),
            self.grid.apple_is_left_safe(safety_limit),
            self.grid.safe_cells_right_global(),
            self.grid.safe_cells_right(),
            self.grid.apple_is_right_safe(safety_limit)
        ])

        # [up_output, down_output, left_output, right_output] = self.dqn.eval(inputs)
        output = self.dqn.eval(inputs)
        if math.isclose(max(output), output[__UP__], rel_tol=1e-9):
            self.grid.change_direction(Direction.up)
        elif math.isclose(max(output), output[__DOWN__], rel_tol=1e-9):
            self.grid.change_direction(Direction.down)
        elif math.isclose(max(output), output[__LEFT__], rel_tol=1e-9):
            self.grid.change_direction(Direction.left)
        else:
            self.grid.change_direction(Direction.right)
        print(output)
        print(max(output))

        if self.is_training:
            reward = torch.tensor([
                self.future_move_reward(Direction.up),
                self.future_move_reward(Direction.down),
                self.future_move_reward(Direction.left),
                self.future_move_reward(Direction.right)
                # self.grid.safe_cells_up_global(),
                # self.grid.safe_cells_down_global(),
                # self.grid.safe_cells_left_global(),
                # self.grid.safe_cells_right_global()
            ])

            self.dqn.add_to_replay_memory(inputs, reward)
            self.dqn.update()

        got_apple = self.grid.next_frame()
        self.actions += 1
        if got_apple:
            self.score += 1

    def future_move_reward(self, direction):
        old_proximity = self.grid.proximity_to_apple()
        grid = copy.deepcopy(self.grid)
        grid.change_direction(direction)
        got_apple = grid.next_frame()
        safe_cells = grid.safe_cells(direction)

        if grid.snake_died():
            return -1.0
        elif got_apple:
            return 1.0
        elif grid.proximity_to_apple() > old_proximity and safe_cells >= 0.5:
            return 0.8
        else:
            return 0.5 * safe_cells

    def perform_split_brain_actions(self):
        """Performs actions using the SplitBrainNetwork."""
        proximity = self.grid.proximity_to_apple()
        inputs = [
            torch.tensor([
                [
                    proximity,
                    self.grid.safe_cells_up_global(),
                    self.grid.safe_cells_up(),
                    self.grid.apple_is_up_safe(0.5)
                ]
            ]),
            torch.tensor([
                [
                    proximity,
                    self.grid.safe_cells_down_global(),
                    self.grid.safe_cells_down(),
                    self.grid.apple_is_down_safe(0.5)
                ]
            ]),
            torch.tensor([
                [
                    proximity,
                    self.grid.safe_cells_left_global(),
                    self.grid.safe_cells_left(),
                    self.grid.apple_is_left_safe(0.5)
                ]
            ]),
            torch.tensor([
                [
                    proximity,
                    self.grid.safe_cells_right_global(),
                    self.grid.safe_cells_right(),
                    self.grid.apple_is_right_safe(0.5)
                ]
            ])
        ]

        new_direction = self.split_brain_network.eval(inputs)
        self.grid.change_direction(new_direction)
        got_apple = self.grid.next_frame()
        new_proximity = self.grid.proximity_to_apple()

        if self.is_training:
            reward = torch.tensor([-0.5])

            if self.grid.snake_died():
                reward = torch.tensor([-1.0])
            elif got_apple:
                reward = torch.tensor([1.0])
            elif new_proximity > proximity:
                reward = torch.tensor([0.8])

            self.split_brain_network.update(reward)

    # TODO: Finish this function
    def perform_QLearn_actions(self, table):
        prevLoc = self.grid.snake.head()
        toApplePrev = self.grid.proximity_to_apple()
        self.grid.snake.direction = table.getMax(prevLoc)
        got_apple = self.grid.next_frame()
        # if snake died, penalty -10
        if self.grid.snake_died():
            self.num += 1
            print("DEAD: " + str(self.num))
            print("LEN: " + str(len(self.grid.snake.body)))
            table.update(prevCell=prevLoc, curCell=None, direction=self.grid.snake.dir_to_int(), reward=-10)
        # if snake got apple, reward 50
        elif got_apple is True:
            curLoc = self.grid.snake.head()
            table.update(prevCell=prevLoc, curCell=curLoc, direction=self.grid.snake.dir_to_int(), reward=50)
        else:
            curLoc = self.grid.snake.head()
            toAppleCur = self.grid.proximity_to_apple()
            # if snake got closer to apple, reward 1
            if toApplePrev < toAppleCur:
                table.update(prevCell=prevLoc, curCell=curLoc, direction=self.grid.snake.dir_to_int(), reward=1)
            # if snake got farther to apple, penalty -1
            else:
                table.update(prevCell=prevLoc, curCell=curLoc, direction=self.grid.snake.dir_to_int(), reward=-1)

    def render(self):
        """Draws the changes to the game-state (if any) to the screen."""
        self._surface.fill(Color('black'))
        for y in range(0, self.height):
            for x in range(0, self.length):
                if self.grid.get_cell(x, y) == CellType.snake:
                    self._surface.blit(self.snake_cell_image,
                                       (x * self.cell_size, y * self.cell_size))
                elif self.grid.get_cell(x, y) == CellType.apple:
                    self._surface.blit(self.apple_cell_image,
                                       (x * self.cell_size, y * self.cell_size))
        pg.display.update()

    def cleanup(self):
        """Quits pygame."""
        pg.quit()

    # TODO: Add win condition.
    def check_for_end_game(self):
        """Checks to see if the snake has died."""
        if self.grid.snake_died():
            self.scores.append(self.score)
            if self.score >= 1:
                self.averages.append(sum(self.scores) / (len(self.averages) + 1))
            # self.plot_scores()
            self.reset()

    def debug_to_console(self):
        """Outputs Debug information to the console."""
        vert = None
        horiz = None
        if self.grid.apple_is_up():
            vert = "Up  "
        elif self.grid.apple_is_down():
            vert = "Down"
        else:
            vert = "None"
        if self.grid.apple_is_left():
            horiz = "Left "
        elif self.grid.apple_is_right():
            horiz = "Right"
        else:
            horiz = "None "
        print(
            "Apple is: (", vert, ",", horiz,
            ")\tProximity: ",
            str(round(self.grid.proximity_to_apple(), 2)), "\t[x, y]:",
            self.grid.snake.head(),
            "   \tUp: (", str(round(self.grid.safe_cells_up(), 2)),
            ",", str(round(self.grid.safe_cells_up_global(), 2)), ")"
            "    \tDown: (", str(round(self.grid.safe_cells_down(), 2)),
            ",", str(round(self.grid.safe_cells_down_global(), 2)), ")"
            "  \tLeft: (", str(round(self.grid.safe_cells_left(), 2)),
            ",", str(round(self.grid.safe_cells_left_global(), 2)), ")"
            "  \tRight: (", str(round(self.grid.safe_cells_right(), 2)),
            ",", str(round(self.grid.safe_cells_right_global(), 2)), ")"
        )

    def play_keyboard_input_game(self):
        """Runs the main game loop using player input."""
        self.reset()
        while(not self._exit):
            pg.event.pump()
            self.clock.tick(self.actions_per_second)
            self.check_for_exit()
            self.perform_keyboard_actions()
            self.check_for_end_game()
            self.render()
            self.debug_to_console()

        self.cleanup()

    def play_split_brain_network_game(self):
        """Runs the main game loop using the SplitBrainNetwork."""
        self.reset()
        while(not self._exit):
            pg.event.pump()
            self.clock.tick(self.actions_per_second)
            self.check_for_exit()
            self.handle_keyboard_input()
            self.perform_split_brain_actions()
            self.split_brain_network.display_outputs()
            self.check_for_end_game()
            self.render()

        self.cleanup()

    def play_DQN_game(self):
        """Runs the main game loop using the Deep Q Network"""
        self.reset()
        while(not self._exit):
            pg.event.pump()
            self.clock.tick(self.actions_per_second)
            self.check_for_exit()
            self.handle_keyboard_input()
            self.perform_DQN_actions()
            self.check_for_end_game()
            self.render()

        self.cleanup()

    def play_QLEARN_game(self):
        """Runs the man game loop using Q Learning"""
        self.reset()
        table = qTable(self.grid.length, self.grid.height, 0.9, 0.9)
        self.num = 0
        while(not self._exit):
            pg.event.pump()
            self.clock.tick(self.actions_per_second)
            self.check_for_exit()
            self.handle_keyboard_input()
            # performs the Q learning for the snake
            self.perform_QLearn_actions(table)
            self.check_for_end_game()
            self.render()

        self.cleanup()
