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


class Board:
    def __init__(self):
        self.state = np.zeros((LENGTH, LENGTH), dtype=int)
        self.actions = [(i, j) for i in range(LENGTH) for j in range(LENGTH)]
        self.x = -1
        self.o = 1
        self.current_player_sign = self.x
        self.winner = None
        self.ended = False
        self.invalid_moves = 0
        self.s = str(self.reset().flatten())

    def reset(self):
        self.state = np.zeros((LENGTH, LENGTH), dtype=int)
        self.current_player_sign = self.x
        self.winner = None
        self.ended = False
        return self.state

    def game_over(self):
        if self.ended:
            self.winner = self.x if self.current_player_sign == self.o else self.o
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
        if np.all((self.state == 0) == False):
            self.winner = None
            self.ended = True
            return True

        return False

    def move(self, action):
        if self.state[action] != 0:
            # self.current_player_sign = self.x if self.current_player_sign == self.o else self.o
            self.invalid_moves += 1
            self.ended = True
            return -10  # Invalid move

        self.state[action] = self.current_player_sign
        reward = 0

        if self.game_over():
            if self.winner == self.current_player_sign:
                reward = 1
            elif self.winner is None:
                reward = 0
            else:
                reward = -1
        else:
            reward = 0

        self.current_player_sign = self.x if self.current_player_sign == self.o else self.o

        return reward

    def draw_board(self):
        num_rows, num_cols = self.state.shape

        for row in range(num_rows):
            print("+" + "-----+" * num_cols)
            for item in range(num_cols):
                print("|", end="")
                if self.state[row, item] == self.x:
                    print("  x  ", end="")
                elif self.state[row, item] == self.o:
                    print("  o  ", end="")
                else:
                    print("     ", end="")
            print("|")
        print("+" + "-----+" * num_cols)
        print()
