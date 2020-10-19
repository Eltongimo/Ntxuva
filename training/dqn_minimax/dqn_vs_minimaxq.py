# Important classes
from agents.minimaxq.minimax_q import MinimaxQPlayer
from game.ntxuva_ttt_game import NtxuvaGame
import sys
from extra_tools.save_data import Save_data
from timeit import default_timer as timer
from agents.dqn.dqn import DqnAgent

# Defining episodes
EPISODES = 100_000

# Initializing the players and trained data
# The Random player is initialized here
minimax_q = MinimaxQPlayer(mark='O', numActionsA=16, numActionsB=16)

dqn_agent = DqnAgent(mark='X')

Q = minimax_q.Q
V = minimax_q.V
pi = minimax_q.pi

# Initializing the game environment
game = NtxuvaGame(player1=dqn_agent, player2=minimax_q)

sys.setrecursionlimit(10000)
FILENAME  = "dqn_vs_minimaxq.p"

# Initializing the statistical data variables
statistical_data = {}
dqn_win = 0
minimax_q_win = 0

# Inidializing the statistical data Object named data_saver
data_saver = Save_data()

start = timer()
# Starting the trainment from episode 0 to the last Episode
episode = 0

NEMS_FILENAME =  "nems_dqn_vs_minimaxq.p"
NOT_NEMS_FILENAME = "not_dqn_vs_minimaxq.p"


for episode in range(EPISODES):
    print(f" -- {episode} -- ")

    winner = game.play()
    # statistics for q_player
    statistical_data[f"{episode}"] = \
        [game.player1.good_moves,
         game.player2.good_moves,
         game.player1.bad_moves,
         game.player2.bad_moves,
         winner.mark if winner is not None else 'd'
         ]

    if isinstance(winner, MinimaxQPlayer):
        minimax_q_win = minimax_q_win + 1
    elif isinstance(winner, DqnAgent):
        dqn_win = dqn_win + 1
    game.reset()
    episode = episode + 1

end = timer()

data_saver.save_models(players={1: minimax_q,
                                2: dqn_agent})

data_saver.save_statistical_data(filepath=FILENAME, statistical_data=statistical_data)

data_saver.save_win_rate(filename=FILENAME, player1_win=dqn_win,
                         player2_win=minimax_q_win)

print(round(end - start, 2))