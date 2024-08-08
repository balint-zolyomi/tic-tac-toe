import random
import numpy as np

import environment

GAMMA = 0.9
ALPHA = 0.2


def max_dict(d):
    max_val = max(d.values())
    max_keys = [key for key, val in d.items() if val == max_val]
    return random.choice(max_keys), max_val


def epsilon_greedy(Q, s, eps):
    if np.random.random() < eps:
        while True:
            a = random.choice(environment.ALL_POSSIBLE_ACTIONS)
            if Q[s][a] != -10:
                return a
    else:
        return max_dict(Q[s])[0]


class Player:
    def __init__(self, board, sign, e):
        self.Q = {tuple(board.state.flatten()): {a: 0 for a in board.actions}}
        self.e = e
        self.sign = sign
        self.board = board
        self.history = []
        self.is_learning = True

    def set_board(self, b):
        self.board = b

    def set_eps(self, e):
        self.e = e

    def set_is_learning(self, is_l):
        self.is_learning = is_l
        self.set_eps(0)

    def set_Q_values(self, s, a, target):
        self.Q[s][a] = target
        for hist_item in self.history[-2::-1]:
            s_prev, a_prev = next(iter(hist_item.items()))
            value = self.Q[s_prev][a_prev] + ALPHA * (GAMMA * target - self.Q[s_prev][a_prev])
            self.Q[s_prev][a_prev] = value
            target = value

    def move(self, state=None):
        if self.is_learning:
            s = tuple(self.board.state.flatten())

            if s not in self.Q:
                self.Q[s] = {a: 0 if self.board.state[a] == 0 else -10 for a in self.board.actions}

            a = epsilon_greedy(self.Q, s, self.e)
            self.history.append({s: a})
            r = self.board.move(a)

            target = r
            if target in (1, -0.1, -10):
                self.set_Q_values(s, a, target)

            return r
        else:
            s = tuple(state.flatten())
            if s not in self.Q:
                self.Q[s] = {a: 0 if s[a] == 0 else -10 for a in self.board.actions}
            a = epsilon_greedy(self.Q, s, self.e)
            return a

    def give_penalty(self, penalty):
        target = penalty
        s, a = next(iter(self.history[-1].items()))
        self.set_Q_values(s, a, target)
