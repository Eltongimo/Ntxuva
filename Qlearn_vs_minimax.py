from players import QPlayer
from ntxuva_ttt_game import NtxuvaGame
import tkinter as tk
import sys
from save_data import Save_data
from minimax import Minimax

data_saver = Save_data()

minimax = Minimax(mark='X')
q_player = QPlayer(mark='O')
q_table = Save_data().load_data(path='q_player_QS.p')


if q_table is not None:
    q_player.Q = q_table
    print ("The qlearn agent has loaded the qtable")

EPISODES = 100_000
sys.setrecursionlimit(10000)

game = NtxuvaGame(master=tk.Tk(), player1=minimax, player2=q_player)


statistical_data = {}
statistical_data_minimax = {}

minimax_win = 0
q_player_win = 0

for episode in range(EPISODES):
    print (f"EPISODE --- {episode} --- ")
    try:

        winner = game.play()
        # statistics for q_player
        statistical_data[episode] = [f"bad-moves: {game.player2.bad_moves}", f"good-moves: {game.player2.good_moves}", f" won: {isinstance(winner,QPlayer)}"]
        statistical_data_minimax[episode] = [f"bad-moves: {game.player1.bad_moves}", f"good-moves: {game.player1.good_moves}",
                                     f"won: {isinstance(winner, Minimax)}"]

        if isinstance(winner, Minimax):
            minimax_win = minimax_win + 1
        else:
            q_player_win = q_player_win + 1

        if episode % 10_000 == 0:
            data_saver.save(prefix='qlearn_minimax', statistical_data=statistical_data, player=game.player2, player1_win=minimax_win, player2_win=q_player_win)
            data_saver.save(prefix='minimax_qlearn', statistical_data=statistical_data_minimax, player=None,
                            player1_win=minimax_win, player2_win=q_player_win)

        game.reset()

    except RecursionError:
        data_saver.save(prefix='qlearn_minimax', statistical_data=statistical_data, player=game.player2,
                        player1_win=minimax_win, player2_win=q_player_win)
        data_saver.save(prefix='minimax_qlearn', statistical_data=statistical_data_minimax, player=None,
                        player1_win=minimax_win, player2_win=q_player_win)
    except MemoryError:
        data_saver.save(prefix='qlearn_minimax', statistical_data=statistical_data, player=game.player2,
                        player1_win=minimax_win, player2_win=q_player_win)
        data_saver.save(prefix='minimax_qlearn', statistical_data=statistical_data_minimax, player=None,
                        player1_win=minimax_win, player2_win=q_player_win)
