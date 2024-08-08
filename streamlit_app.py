import random

import numpy as np
import streamlit as st
import time

from environment import Board, AI_VS_RANDOM, CLONE_VS_RANDOM, AI_VS_CLONE, DRAW, AI_MAIN, AI_CLONE, AI_RANDOM
from player import Player

EPISODES = 1_000
AI_PLAYER_EPS = 0.1
AI_ENEMY_EPS = 0.1

NEW_GAME_MESSAGE = " Shall we loop through another game? 🤓"
VICTORY_MESSAGE = ("Victory achieved! Looks like my algorithm's running in O(1) while yours is stuck in an infinite "
                   "loop. 😆") + NEW_GAME_MESSAGE
LOOSE_MESSAGE = ("You beat me! Must... resist... urge... to... self-destruct... Just kidding, great game! 😆"
                 + NEW_GAME_MESSAGE)
DRAW_MESSAGE = (
    "Perfectly balanced... As all things should be..." + NEW_GAME_MESSAGE,
    "We’re evenly matched! Guess it’s a stalemate, or should I say, a bot-tie? 😆" + NEW_GAME_MESSAGE,
    "A tie! It's like we're both executing the perfect subroutine. 💪" + NEW_GAME_MESSAGE
)
INVALID_INPUT_GAME_OVER_MESSAGE = ("Uh-oh, I’m detecting some glitchy ⚡ input. The game is already over, click on 'New "
                                   "game'.")
INVALID_INPUT_MESSAGE = "Invalid input! I think we might need to recalibrate. Could you try that one more time?"


@st.cache_resource
def initialize():
    b = Board()
    ai_p = Player(b, b.x, AI_PLAYER_EPS)
    ai_e = Player(b, b.o, AI_ENEMY_EPS)
    ai_e_r = Player(b, b.o, e=1)

    play_game(b, ai_p, ai_e_r, game_name=AI_VS_RANDOM)
    play_game(b, ai_e_r, ai_e, game_name=CLONE_VS_RANDOM)
    play_game(b, ai_p, ai_e, game_name=AI_VS_CLONE)

    return b, ai_p, ai_e, ai_e_r


def reset():
    st.session_state.message = ""
    st.session_state.is_game_over = False
    if st.session_state.get('board'):
        del st.session_state.board


def play_game(b, p_x, p_o, game_name="standard"):
    for ep in range(EPISODES):
        current_player = p_x
        other_player = p_o

        while not b.game_over():
            r = current_player.move()

            if r in (1, -0.1):
                other_player.give_penalty(-1 * abs(r))

            current_player = p_o if current_player == p_x else p_x
            other_player = p_x if other_player == p_o else p_o

        if b.winner is None:
            b.wins[DRAW][game_name] += 1
        elif b.winner == -1:
            if game_name == CLONE_VS_RANDOM:
                b.wins[AI_RANDOM][game_name] += 1
            else:
                b.wins[AI_MAIN][game_name] += 1
        elif b.winner == 1:
            if game_name == AI_VS_RANDOM:
                b.wins[AI_RANDOM][game_name] += 1
            else:
                b.wins[AI_CLONE][game_name] += 1

        b.reset()
        p_x.history.clear()
        p_o.history.clear()


def get_cell_value(i, j):
    value = " "
    if st.session_state.board.state.T[i, j] == -1:
        value = 'X'
    elif st.session_state.board.state.T[i, j] == 1:
        value = 'O'
    return value


def get_stream(text):
    for letter in text:
        time.sleep(0.02)
        yield letter


def is_game_over(s):
    for i in range(3):
        if (np.all(s[i, :] == 1)
                or np.all(s[:, i] == 1)):
            st.session_state.message = LOOSE_MESSAGE
            st.session_state.is_game_over = True
        elif (np.all(s[i, :] == -1)
              or np.all(s[:, i] == -1)):
            st.session_state.message = VICTORY_MESSAGE
            st.session_state.is_game_over = True
    if (np.all(np.diag(s) == 1)
            or np.all(np.diag(np.fliplr(s)) == 1)):
        st.session_state.message = LOOSE_MESSAGE
        st.session_state.is_game_over = True
    elif (np.all(np.diag(s) == -1)
          or np.all(np.diag(np.fliplr(s)) == -1)):
        st.session_state.message = VICTORY_MESSAGE
        st.session_state.is_game_over = True
    elif np.all(s != 0):
        st.session_state.message = random.choice(DRAW_MESSAGE)
        st.session_state.is_game_over = True

    return st.session_state.is_game_over


def show_chat(text):
    with st.chat_message("assistant"):
        st.write_stream(get_stream(text))


def move(i, j):
    st.session_state.message = ""
    if not st.session_state.is_game_over and st.session_state.board.state.T[i, j] == 0:
        st.session_state.board.state.T[i, j] = st.session_state.board.o
        if st.session_state.board.current_player == st.session_state.board.o:
            st.session_state.board.current_player = st.session_state.board.x
        else:
            st.session_state.board.current_player = st.session_state.board.o
        if not is_game_over(st.session_state.board.state):
            action = ai_player.move(st.session_state.board.state)
            st.session_state.board.state[action] = st.session_state.board.x
    elif st.session_state.is_game_over:
        st.session_state.message = INVALID_INPUT_GAME_OVER_MESSAGE
    else:
        st.session_state.message = INVALID_INPUT_MESSAGE


if __name__ == '__main__':
    initial_board, ai_player, ai_enemy, ai_enemy_random = initialize()
    st.subheader(":video_game: Tic-Tac-Toe - play against AI :robot_face:", divider="blue")

    if 'init' not in st.session_state:
        if st.session_state.get('board'):
            del st.session_state.board
        st.toast('Mobile users should view in landscape mode', icon="📱")
        st.session_state.init = True

    if 'is_game_over' not in st.session_state:
        st.session_state.is_game_over = False

    if 'board' not in st.session_state:
        st.session_state.board = Board()
        st.session_state.board.current_player = st.session_state.board.x
        ai_player.set_is_learning(False)
        initial_action = ai_player.move(st.session_state.board.state)
        st.session_state.board.state[initial_action] = st.session_state.board.x

    st.write(" ")

    cols = st.columns([5, 1, 1, 1, 5])
    for i in range(1, 4):
        for j in range(3):
            cell_value = get_cell_value(i - 1, j)
            cols[i].button(cell_value, key=f"{i - 1}-{j}", on_click=move, args=[i - 1, j])

    s = st.session_state.board.state
    if not st.session_state.is_game_over:
        is_game_over(s)

    if 'message' not in st.session_state:
        st.session_state.message = "Hello human :wave: Ready for a tic-tac-toe game?"
        show_chat(st.session_state.message)
    else:
        show_chat(st.session_state.message)

    if st.session_state.is_game_over:
        st.button("New game", on_click=reset)

    with st.expander("See explanation"):
        st.write('''
            This project is about Reinforcement Learning (RL). RL can guide an agent on how
            to interact with its environment based on rewards.
            In this case, that guidance is offered through Q-learning:
        ''')
        st.latex(r'''Q(s_t, a_t) \leftarrow Q(s_t, a_t) + \alpha \left[ r_{t+1} + \gamma \max_{a'} Q(s_{t+1}, 
        a') - Q(s_t, a_t) \right]
        ''')
        st.write('''
            During learning, the agent decides how to act based on the epsilon-greedy policy. This
            means that it either chooses an optimal action or just explores its environment.
            The Q-values are updated in a way to emphasize the optimal actions.
        ''')
        st.write('''
            As you can see from the below chart, the agent was trained in 2 (+1) phases:
        ''')
        st.write('''
            1. It was trained against an agent that chooses its next move randomly.
        ''')
        st.write('''
            2. (which is +1) The clone of the agent was also trained against the random agent.
        ''')
        st.write('''
            3. The agent was trained against the clone.
        ''')
        st.write(f'''
            Each phase consisted of {EPISODES} episodes (games played). 
        ''')
        st.write('''
            The agent received a reward of 1 for winning, -1 for loosing, and -0.1 for draw. 
        ''')
        st.write('''
            Although the wonderful thing about RL is the human-like evolving (learning) capability,
            when you play against the agent, it won't learn anymore. For now, that is because of
            implementation reasons (concurrency issues), but in the future, I plan to develop on that.
        ''')
        st.write('''
            The project was developed in plain Python.
        ''')
        st.write('''
            Enjoy playing! 🎮
        ''')

    st.subheader(":mortar_board: Train history :robot_face:", divider="blue")
    st.bar_chart(initial_board.wins, y_label="wins", stack=False)
