# -*- coding: utf-8 -*-
"""
Created on Thu Sep  3 01:51:46 2020

@author: EltonUG
"""

# Important classes
from agents.dqn.dqn import DqnAgent
from agents.minimax.minimax import RandomPlayer
from game.ntxuva_ttt_game import NtxuvaGame
import tkinter as tk
import sys
from extra_tools.save_data import Save_data


FILENAME = "minimax_vs_dqn"

# Defining episodes
EPISODES = 5_000

# Initializing the players and trainded data
# The Random player is initialized here
minimax = RandomPlayer(mark='X', prof=3)
dqn = DqnAgent(mark='O')

# Initializing the game environment
game = NtxuvaGame(master=tk.Tk(), player1=minimax, player2=dqn)

sys.setrecursionlimit(10000)

# Initializing the statistical data variables
statistical_data = {}
dqn_win = 0
minimax_player_win = 0

# Inidializing the statistical data Object named data_saver
data_saver = Save_data()

from timeit import default_timer as timer
start = timer()
# Starting the trainment from episode 0 to the last Episode
for episode in range(EPISODES):


    print(f"-- {episode} -- ")
    # After 100.000 episodes, we save the statistical data and the trained model til here.
    if episode % 500 == 0:

        data_saver.save_models(players={1: minimax,
                                        2: dqn})

        data_saver.save_statistical_data(filepath=FILENAME, statistical_data=statistical_data)

        data_saver.save_win_rate(filename=FILENAME, player1_win=minimax_player_win,
                                 player2_win=dqn_win)

    try:

        winner = game.play()
        # statistics for dqn
        statistical_data[f"{episode}"] = \
            [
                f"{game.player1.good_moves}",
                f"{game.player2.good_moves}",
                f"{game.player1.bad_moves}",
                f"{game.player2.bad_moves}",
                f"{winner.mark if winner is not None else 'd'}"
            ]

        if isinstance(winner, DqnAgent):
            dqn_win = dqn_win + 1
        else:
            minimax_player_win = minimax_player_win + 1

        game.reset()

    except RecursionError:

        data_saver.save_models(players={1: game.player1,
                                        2: game.player2})

        data_saver.save_statistical_data(filepath=FILENAME, statistical_data=statistical_data)

        data_saver.save_win_rate(filename=FILENAME, player1_win=minimax_player_win,
                                 player2_win=dqn_win)

    except MemoryError:
        data_saver.save_models(players={1: game.player1,
                                        2: game.player2})

        data_saver.save(prefix=FILENAME, statistical_data=statistical_data,
                        player1_win=minimax_player_win, player2_win=dqn_win)

        data_saver.save_statistical_data(filepath=FILENAME, statistical_data=statistical_data)

        data_saver.save_win_rate(filename=FILENAME, player1_win=minimax_player_win,
                                 player2_win=dqn_win)

data_saver.save_models(players={1: minimax,
                                2: dqn})

data_saver.save_statistical_data(filepath=FILENAME, statistical_data=statistical_data)

data_saver.save_win_rate(filename=FILENAME, player1_win=minimax_player_win, player2_win=dqn_win)

print (f"tempo levado --- {timer() - start}")
