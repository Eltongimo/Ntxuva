# Important classes
from game.ntxuva_ttt_game import NtxuvaGame
from extra_tools.save_data import Save_data
from timeit import default_timer as timer
from agents.qplayerandothers.players import QPlayer,RandomPlayer

start = timer()

EPISODES = 2

data_saver = Save_data(filename='qplayer_vs_random')

game = NtxuvaGame(player1=RandomPlayer(mark='X',rating=1000), player2=QPlayer(mark='O', rating=1000))

for episode in range(EPISODES):

    print(f" -- {episode} -- ")

    winner = game.play()

    if winner is not None:
        winner.wins = winner.wins + 1

    game.reset()
#
# data_saver.save(players={1: game.player1,
#                          2: game.player2})

data_saver.save_elo({1: game.player1, 2: game.player2})
end = timer()

print (f"completed in {round(end - start,2)} seconds!")