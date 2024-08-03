import matplotlib.pyplot as plt

from environment import Board
from player import Player
from human import Human

EPISODES = 500_000


def state_to_string(state):
    return str(state.flatten())


if __name__ == '__main__':
    board = Board()
    aiPlayer = Player(board, board.x)
    aiEnemy = Player(board, board.o)

    steps = {}
    wins = {"=": 0, "x": 0, "o": 0}
    for i in range(EPISODES):
        if i % 10_000 == 0:
            print(i)

        current_player = aiPlayer

        while not board.game_over():
            r = current_player.move()

            current_player = aiEnemy if current_player == aiPlayer else aiPlayer

        if board.winner is None:
            wins["="] += 1
        elif board.winner == 1:
            wins["o"] += 1
        elif board.winner == -1:
            wins["x"] += 1
        board.reset()

    print(wins)
    print("invalid moves:", str(int(board.invalid_moves / EPISODES * 100)) + " %")
    plt.bar(list(wins.keys()), list(wins.values()))
    plt.show()

    human = Human(board)
    current_player = aiPlayer
    while not board.game_over():
        current_player.move()
        board.draw_board()
        current_player = human if current_player == aiPlayer else aiPlayer
