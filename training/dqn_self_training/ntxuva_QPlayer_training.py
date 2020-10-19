import tkinter as tk
import sys
import pickle as pickle    # cPickle is for Python 2.x only; in Python 3, simply "import pickle" and the accelerated version will be used automatically if available
from game.ntxuva_ttt_game import NtxuvaGame, DqnAgent

tk.wantobjects = False
root = tk.Tk()
epsilon = 0.9
player1 = DqnAgent(mark="X", epsilon=epsilon)
player2 = DqnAgent(mark="O", epsilon=epsilon)
game = NtxuvaGame(root, player1, player2)

sys.setrecursionlimit(10000)

N_episodes = 45000

for episodes in range(N_episodes):
    print('Episode ', episodes)

    try:
        game.play()
    except RecursionError:
        Q = game.Q
        filename = "Q_table_ntxuva_dictionary_%s.p" % episodes
        pickle.dump(Q, open(filename, "wb"))
    except MemoryError:
        Q = game.Q
        filename = "Q_table_ntxuva_dictionary_%s.p" % episodes
        pickle.dump(Q, open(filename, "wb"))
    game.reset()

Q = game.Q

filename = "Q_table_ntxuva_dictionary_%s.p" % N_episodes
pickle.dump(Q, open(filename, "wb"))
