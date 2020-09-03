from players import QPlayer
from dqn import DqnAgent
from ntxuva_ttt_game import NtxuvaGame
import tkinter as tk
import sys
from save_data import Save_data

EPISODES = 100_000

dqn = DqnAgent(mark='X')

q_table = Save_data().load_data(path='q_player_QS.p')

q_player = QPlayer(mark='O', Q=q_table)

game = NtxuvaGame(master=tk.Tk(), Q=q_table , player1=dqn, player2=q_player)

sys.setrecursionlimit(10000)

statistical_data = {}
q_player_win = 0
dqn_player_win = 0

data_saver = Save_data()

for episode in range(EPISODES):
    
    if episode % 100_000:
        data_saver.save_models({1: game.player1, 2:game.player2 }, episode=episode)
    print(f"Episode -- {episode} -- ")

    try:

        winner = game.play()
        # statistics for q_player
        statistical_data[f"episode #{episode}"] = \
            [
             f"p1-good-moves:  {game.player1.good_moves}",
             f"p2-good-moves:  {game.player2.good_moves}",
             f"p1-bad-moves:   {game.player1.bad_moves}",
             f"p2-bad-moves:   {game.player2.bad_moves}",
             f"won: {winner.mark if winner is not None else 'd'}"
            ]

        
        if isinstance(winner, QPlayer):
            q_player_win = q_player_win + 1
        else:
            dqn_player_win = dqn_player_win + 1

        game.reset()
    except RecursionError:

        data_saver.save_models(players={1: game.player1,
                                        2: game.player2})

        data_saver.save_statistical_data(filepath='dqn_vs_qlearner', statistical_data=statistical_data)

        data_saver.save_win_rate(filename='dqn_vs_qlearner', player1_win=dqn_player_win, player2_win=q_player_win)

    except MemoryError:
            data_saver.save_models(players={1: game.player1,
                                            2: game.player2 })

            data_saver.save(prefix='dqn_vs_qlearner', statistical_data=statistical_data,
                            player1_win=dqn_player_win, player2_win=q_player_win)

            data_saver.save_statistical_data(filepath='dqn_vs_qlearner',statistical_data=statistical_data)

            data_saver.save_win_rate(filename='dqn_vs_qlearner', player1_win=dqn_player_win, player2_win=q_player_win)


data_saver.save_models(players={1: dqn,
                                2: q_player })

data_saver.save_statistical_data(filepath='dqn_vs_qlearner',statistical_data=statistical_data)

data_saver.save_win_rate(filename='dqn_vs_qlearner', player1_win=dqn_player_win, player2_win=q_player_win)