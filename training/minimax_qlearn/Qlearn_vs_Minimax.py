# Important classes
from game.ntxuva_ttt_game import NtxuvaGame
from extra_tools.save_data import Save_data
from timeit import default_timer as timer
from agents.minimax.minimax import Minimax
from agents.qplayerandothers.players import QPlayer

start = timer()

EPISODES = 10

qplayer_win = 0

minimax_win = 0

statistical_data = {}

data_saver = Save_data()

minimax = Minimax(mark='X', prof=5)

qplayer = QPlayer(mark='O')

FILENAME  = 'qplayer_vs_minimax'

game = NtxuvaGame(player1=minimax, player2=qplayer)

for episode in range(EPISODES):

    print(f" -- {episode} -- ")

    winner = game.play()

    statistical_data[f"{episode}"] = \
        [game.player1.good_moves,
         game.player2.good_moves,
         game.player1.bad_moves,
         game.player2.bad_moves,
         winner.mark if winner is not None else 'd'
         ]

    if isinstance(winner, Minimax):
        minimax_win = minimax_win + 1
    elif isinstance(winner,QPlayer):
        qplayer_win = qplayer_win + 1
    game.reset()
    game.warm_up_time = episode

data_saver.save_statistical_data(filepath=FILENAME, statistical_data=statistical_data)
data_saver.save_win_rate(filename=FILENAME, player1_win=qplayer_win, player2_win=minimax_win)
data_saver.save_models(players={1: qplayer,
                                2: minimax})
end = timer()
print (f"completed in {round(end - start,2)} seconds!")