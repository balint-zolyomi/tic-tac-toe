import matplotlib.pyplot as plt

from environment import Board
from player import Player
from human import Human

EPISODES = 10_000
AI_PLAYER_EPS = 0.1
AI_ENEMY_EPS = 0.1


def play_game(b, p_x, p_o, game_name="standard"):
    b.wins[game_name + "_="] = 0
    b.wins[game_name + "_x"] = 0
    b.wins[game_name + "_o"] = 0

    for i in range(EPISODES):
        if i % (EPISODES / 100) == 0:
            print(f"{game_name}_ep:", int(i / EPISODES * 100), "%")

        current_player = p_x
        other_player = p_o

        while not b.game_over():
            r = current_player.move()

            if r in (1, -0.1):
                other_player.give_penalty(-1 * abs(r))

            current_player = p_o if current_player == p_x else p_x
            other_player = p_x if other_player == p_o else p_o

        if b.winner is None:
            b.wins[game_name + "_="] += 1
        elif b.winner == -1:
            b.wins[game_name + "_x"] += 1
        elif b.winner == 1:
            b.wins[game_name + "_o"] += 1

        b.reset()
        ai_player.history.clear()
        ai_enemy.history.clear()


def play_with_human(b, ai, human):
    while True:
        current_player = ai
        b.reset()
        b.draw_board()
        while not b.game_over():
            current_player.move()
            b.draw_board()
            current_player = human if current_player == ai else ai
        answer = input("Continue playing? (y/n) ")
        if answer and answer.lower() == 'n':
            break


if __name__ == '__main__':
    board = Board()
    ai_player = Player(board, board.x, AI_PLAYER_EPS)
    ai_enemy = Player(board, board.o, AI_ENEMY_EPS)
    ai_enemy_random = Player(board, board.o, e=1)
    human_player = Human(board)

    play_game(board, p_x=ai_player, p_o=ai_enemy_random, game_name="r_train_x")
    play_game(board, p_x=ai_enemy_random, p_o=ai_enemy, game_name="r_train_o")
    play_game(board, p_x=ai_player, p_o=ai_enemy, game_name="ai_train")

    ai_player.set_eps(0)
    ai_enemy.set_eps(0)
    play_game(board, p_x=ai_player, p_o=ai_enemy_random, game_name="test_x")
    play_game(board, p_x=ai_enemy_random, p_o=ai_enemy, game_name="test_o")

    print("wins:", board.wins)
    plt.bar(list(board.wins.keys()), list(board.wins.values()))
    plt.show()

    # play_with_human(board, ai=ai_player, human=human_player)
