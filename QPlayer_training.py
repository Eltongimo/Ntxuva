from players import RandomPlayer, QPlayer
from ntxuva_ttt_game import NtxuvaGame
import tkinter as tk
import sys
from save_data import Save_data


data_saver = Save_data()

random_player = RandomPlayer(mark='X')
q_player = QPlayer(mark='O')

q_table = Save_data().load_data(path='q_player_QS1.p')

if q_table is not None:
    q_player.Q = q_table

EPISODES = 600_000
sys.setrecursionlimit(10000)

game = NtxuvaGame(master=tk.Tk(), Q=q_player.Q, 
                  player1=random_player, player2=q_player)

statistical_data = {}
random_win = 0
q_player_win = 0

for episode in range(EPISODES):
    if episode % 50_000 == 0:
        print(f"episode --- {episode}")
        data_saver.save_models({1: game.player1, 2:game.player2 }, episode=episode)
    try:

        winner = game.play()
        # statistics for q_player
        statistical_data[f"{episode}"] = \
            [
             f"p1-good-moves:  {game.player1.good_moves}\n",
             f"p2-good-moves:  {game.player2.good_moves}\n",
             f"p1-bad-moves:   {game.player1.bad_moves}\n",
             f"p2-bad-moves:   {game.player2.bad_moves}\n",
             f"won: {winner.mark if winner is not None else 'd'}\n"
            ]

        
        if isinstance(winner, QPlayer):
            q_player_win = q_player_win + 1
        else:
            random_win = random_win + 1

        game.reset()
    except RecursionError:

        data_saver.save_models(players={1: game.player1,
                                        2: game.player2})

        data_saver.save_statistical_data(filepath='dqn_vs_qlearner', statistical_data=statistical_data)

        data_saver.save_win_rate(filename='dqn_vs_qlearner', player1_win=random_win, player2_win=q_player_win)

    except MemoryError:
            data_saver.save_models(players={1: game.player1,
                                            2: game.player2 })

            data_saver.save(prefix='dqn_vs_qlearner', statistical_data=statistical_data,
                            player1_win=random_win, player2_win=q_player_win)

            data_saver.save_statistical_data(filepath='dqn_vs_qlearner',statistical_data=statistical_data)

            data_saver.save_win_rate(filename='dqn_vs_qlearner', player1_win=random_win,
                                     player2_win=q_player_win)


data_saver.save_models(players={1: random_player,
                                2: q_player })

data_saver.save_statistical_data(filepath='dqn_vs_qlearner',statistical_data=statistical_data)

data_saver.save_win_rate(filename='dqn_vs_qlearner', player1_win=random_win, player2_win=q_player_win)

