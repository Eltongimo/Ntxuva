import json
import pickle
from players import QPlayer
from dqn import  DqnAgent

class Save_data:

    def __init__(self):
        pass

    def save(self,prefix,statistical_data, players, player1_win, player2_win ):
        self.save_model(player=players)
        self.save_win_rate(file=prefix,player1_win=player1_win,player2_win=player2_win)
        self.save_statistical_data(file=prefix,statistical_data=statistical_data)

    def save_win_rate(self, filename,player1_win, player2_win):
        with open(f"{filename}_win_rate_data.json", 'w') as f:
            json.dump({"player1": player1_win,
                       "player2": player2_win
                       }, f, indent=2)

    def save_statistical_data(self,filepath,statistical_data):
        with open(f"{filepath}_statistical_data.json", 'w') as fp:
            json.dump(statistical_data, fp, indent=2)


    def save_models(self, players, episode=0):

        if isinstance(players[1], QPlayer):
            filename = f"q_player_QS_{episode}.p"
            pickle.dump(players[1].Q, open(filename, "wb"))

        if isinstance(players[2], QPlayer):
            filename = f"q_player_QS_{episode}.p"
            pickle.dump(players[2].Q, open(filename, "wb"))

        if  isinstance(players[1], DqnAgent):
            players[1].save_weights(f'dqn_model_{episode}.h5')

        if isinstance(players[2], DqnAgent):
            players[2].save_weights(f'dqn_model_{episode}.h5')


    def load_data(self, path):
        try:
            return pickle.load(open(path, "rb"))
        except:
            return {}
