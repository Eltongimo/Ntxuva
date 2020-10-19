import tkinter as tk

import pickle as pickle    # cPickle is available in Python 2.x only, otherwise use pickle
from ttt_game import Game
from agents.qplayerandothers.players import HumanPlayer, DqnAgent

tk.wantobjects = False

Q = pickle.load(open("Q_table_dictionary.p", "rb"))

root = tk.Tk()
player1 = HumanPlayer(mark="X")
player2 = DqnAgent(mark="O", epsilon=0)

game = Game(root, player1, player2, Q=Q)

game.play()
root.mainloop()
