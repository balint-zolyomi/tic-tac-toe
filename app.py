import matplotlib.pyplot as plt

from environment import Board
from player import Player


def state_to_string(state):
    return str(state.flatten())


if __name__ == '__main__':
    board = Board()
    player = Player(board, board.x)
    enemy = Player(board, board.o)
    # board.draw_board()

    # Initialize Q-table
    # Q1 = {}
    # actions = board.actions
    # Q1[str(board.state.flatten())] = {a: 0 for a in actions}
    #
    # Q2 = {}
    # actions = board.actions
    # Q2[str(board.state.flatten())] = {a: 0 for a in actions}

    # reward_per_episode = []
    steps = {}
    wins = {"=": 0, "x": 0, "o": 0}
    for i in range(10):
        if i % 1000 == 0:
            print(i)
        # print("Episode:", i)

        # s = str(board.reset().flatten())
        # episode_reward = 0
        steps_per_episode = 0
        current_player = player

        while not board.game_over():
            # board.draw_board()
            current_player.move()

            # a = epsilon_greedy(Q, s)
            # r = board.move(a)
            # s2 = str(board.state.flatten())
            #
            # if s2 not in Q:
            #     Q[s2] = {a: 0 for a in actions}
            #
            # # episode_reward += r
            #
            # maxQ = max_dict(Q[s2])[1]
            # Q[s][a] = Q[s][a] + ALPHA * (r + GAMMA * maxQ - Q[s][a])

            # s = s2

            current_player = enemy if current_player == player else player

        # if steps_per_episode not in steps:
        #     steps[steps_per_episode] = 1
        # else:
        #     steps[steps_per_episode] += 1
        # reward_per_episode.append(episode_reward)
        # board.draw_board()
        # if i % 100 == 1:
            # board.draw_board()
            # print(board.winner)
        if board.winner is None:
            wins["="] += 1
        elif board.winner == 1:
            wins["o"] += 1
        elif board.winner == -1:
            wins["x"] += 1
        board.reset()
        # print(f"Total reward for episode {i}: {episode_reward}")
    print(wins)
    plt.bar(list(wins.keys()), list(wins.values()))
    # plt.bar(list(steps.keys()), list(steps.values()))
    plt.show()

    # policy = {}
    # V = {}
    #
    # for s in Q1.keys():
    #     a, max_q = max_dict(Q1[s])
    #     policy[s] = a
    #     V[s] = max_q
    #
    # print("values:")
    # print(V)
    # print("policy:")
    # print(policy)
    #
    # while True:
    #     board.draw_board()
    #     a = policy[str(board.state.flatten())]
    #     board.move(a)
    #     if board.game_over():
    #         board.draw_board()
    #         break
    # print("Reward per episode:", reward_per_episode)
