import random
import numpy as np

import environment

GAMMA = 1
ALPHA = 0.01


def max_dict(d):
    max_val = max(d.values())
    max_keys = [key for key, val in d.items() if val == max_val]
    return random.choice(max_keys), max_val


def epsilon_greedy(Q, s, eps=0.2):
    if np.random.random() < eps:
        return random.choice(environment.ALL_POSSIBLE_ACTIONS)
    else:
        a_opt = max_dict(Q[s])[0]
        # print("Q", Q)
        # print("a_opt", a_opt)
        return a_opt


class Player:
    def __init__(self, board, sign):
        self.Q = {str(board.state.flatten()): {a: 0 for a in board.actions}}
        self.sign = sign
        self.board = board

    def move(self):
        s = str(self.board.state.flatten())

        if s not in self.Q:
            self.Q[s] = {a: 0 for a in self.board.actions}

        a = epsilon_greedy(self.Q, self.board.s)
        r = self.board.move(a)
        s2 = str(self.board.state.flatten())

        if s2 not in self.Q:
            self.Q[s2] = {a: 0 for a in self.board.actions}

        # episode_reward += r

        maxQ = max_dict(self.Q[s2])[1]
        self.Q[s][a] = self.Q[s][a] + ALPHA * (r + GAMMA * maxQ - self.Q[s][a])

    def print_policy(self):
        policy = {}
        V = {}

        for s in self.Q.keys():
            a, max_q = max_dict(self.Q[s])
            policy[s] = a
            V[s] = max_q

        print("values:")
        print(V)
        print("policy:")
        print(policy)

        # while True:
        #     board.draw_board()
        #     a = policy[str(board.state.flatten())]
        #     board.move(a)
        #     if board.game_over():
        #         board.draw_board()
        #         break
