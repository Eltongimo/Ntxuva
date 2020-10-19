# Important classes
from agents.minimax.minimax import RandomPlayer
from agents.minimaxq.minimax_q import MinimaxQPlayer
from game.ntxuva_ttt_game import NtxuvaGame
import sys
from extra_tools.save_data import Save_data
from timeit import default_timer as timer

# Defining episodes
EPISODES = 5_000

# Initializing the players and trainded data
# The Random player is initialized here
minimax_q = MinimaxQPlayer(mark='O', numActionsA=16, numActionsB=16)
minimax = RandomPlayer(mark='X', prof=1)
Q = minimax_q.Q
V = minimax_q.V
pi = minimax_q.pi

# Initializing the game environment
game = NtxuvaGame(player1=minimax, player2=minimax_q)

sys.setrecursionlimit(10000)
FILENAME  = "minimax_vs_minimaxq"

# Initializing the statistical data variables
statistical_data = {}
minimax_win = 0
minimax_q_win = 0

# Inidializing the statistical data Object named data_saver
data_saver = Save_data()

start = timer()
# Starting the trainment from episode 0 to the last Episode
episode = 0

NEMS_FILENAME =  "nems_minimax_vs_minimaxq.p"
NOT_NEMS_FILENAME = "not_nems_minimax_vs_minimaxq.p"

while episode < EPISODES:

    print(f" -- {episode} -- ")

    # After 100.000 episodes, we save the statistical data and the trained model til here.
    if episode % 500 == 0:
        data_saver.save_statistical_data(filepath=FILENAME, statistical_data=statistical_data)
        data_saver.save_win_rate(filename=FILENAME, player1_win=minimax_win,
                                 player2_win=minimax_q_win)

    winner = game.play()
    statistical_data[f"{episode}"] = \
        [game.player1.good_moves,
         game.player2.good_moves,
         game.player1.bad_moves,
         game.player2.bad_moves,
         winner.mark if winner is not None else 'd'
         ]

    if isinstance(winner, MinimaxQPlayer):
        minimax_q_win = minimax_q_win + 1
    elif isinstance(winner, RandomPlayer):
        minimax_win = minimax_win + 1
    game.reset()
    episode = episode + 1
    game.warm_up_time = episode

data_saver.dump_not_nems(filename=NOT_NEMS_FILENAME, the_set=game.ntxuva.not_never_ending_moves)
data_saver.save_statistical_data(filepath=FILENAME, statistical_data=statistical_data)
data_saver.save_win_rate(filename=FILENAME, player1_win=minimax_win, player2_win=minimax_q_win)
data_saver.save_models(players={1: minimax,
                                2: minimax_q})
end = timer()
print(round(end - start, 2))