import tkinter as tk

import pickle as pickle    # cPickle is available in Python 2.x only, otherwise use pickle
from ntxuva_ttt_game import NtxuvaGame
from players import Player, HumanPlayer, ComputerPlayer, RandomPlayer, QPlayer

tk.wantobjects = False

Q = pickle.load(open("q_player_QS.p", "rb"))
# Q = {}
root = tk.Tk()
# player1 = HumanPlayer(mark="X")
# player2 = RandomPlayer(mark="O")

player1 = HumanPlayer(mark="X")
player2 = QPlayer(mark="O",Q=Q)

game = NtxuvaGame(root, player1, player2, Q=Q)

game.play()
root.mainloop()