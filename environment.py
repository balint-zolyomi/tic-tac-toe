import numpy as np

LENGTH = 3
ALL_POSSIBLE_ACTIONS = (
    (0, 0),
    (0, 1),
    (0, 2),
    (1, 0),
    (1, 1),
    (1, 2),
    (2, 0),
    (2, 1),
    (2, 2),
)
AI_VS_RANDOM = "1. ai vs. random"
CLONE_VS_RANDOM = "2. clone vs. random"
AI_VS_CLONE = "3. ai vs. clone"
DRAW = "draw"
AI_MAIN = "ai main"
AI_CLONE = "ai clone"
AI_RANDOM = "ai random"


class Board:
    def __init__(self):
        self.state = np.zeros((LENGTH, LENGTH), dtype=int)
        self.actions = [(i, j) for i in range(LENGTH) for j in range(LENGTH)]
        self.x = -1
        self.o = 1
        self.current_player = self.x
        self.winner = None
        self.ended = False
        self.wins = {
            DRAW: {AI_VS_RANDOM: 0, CLONE_VS_RANDOM: 0, AI_VS_CLONE: 0},
            AI_CLONE: {CLONE_VS_RANDOM: 0, AI_VS_CLONE: 0},
            AI_MAIN: {AI_VS_RANDOM: 0, AI_VS_CLONE: 0},
            AI_RANDOM: {AI_VS_RANDOM: 0, CLONE_VS_RANDOM: 0}
        }

    def reset(self):
        self.state = np.zeros((LENGTH, LENGTH), dtype=int)
        self.current_player = self.x
        self.winner = None
        self.ended = False
        return self.state

    def game_over(self):
        if self.ended:
            return True

        # rows
        for i in range(LENGTH):
            for player in (self.x, self.o):
                if self.state[i].sum() == player * 3:
                    self.winner = player
                    self.ended = True
                    return True

        # columns
        for j in range(LENGTH):
            for player in (self.x, self.o):
                if self.state[:, j].sum() == player * 3:
                    self.winner = player
                    self.ended = True
                    return True

        # diagonals
        for player in (self.x, self.o):
            if self.state.trace() == player * 3 or np.fliplr(self.state).trace() == player * 3:
                self.winner = player
                self.ended = True
                return True

        # draw
        if np.all(self.state != 0):
            self.winner = None
            self.ended = True
            return True

        return False

    def move(self, action):
        if self.state[action] != 0:
            self.ended = True
            self.winner = self.x if self.current_player == self.o else self.o
            return -10  # Invalid move

        self.state[action] = self.current_player

        if self.game_over():
            if self.winner == self.current_player:
                reward = 1
            elif self.winner is None:
                reward = -0.1
            else:
                reward = -1
        else:
            reward = 0

        self.current_player = self.x if self.current_player == self.o else self.o

        return reward
