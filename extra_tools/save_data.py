import json
from agents.dqn.dqn import DqnAgent
import os

class Save_data:

    def __init__(self, filename = '.p'):
        self.filename = filename
        self.FOLDER_PATH = r'C:\\Users\\EltonUG\\Desktop\\numba optimized\\Ntxuva\\elo_ratings'

    def save(self, players ):
        self.save_win_rate(player1_win=players[1].wins,player2_win=players[2].wins)
        self.save_models(players)

    def save_win_rate(self,player1_win, player2_win):
        with open(f"{self.filename}_win_rate_data.json", 'w') as f:
            json.dump({"player1": player1_win,
                       "player2": player2_win
                       }, f, indent=2)

    def save_models(self, players):

        if isinstance(players[1], DqnAgent):
            players[1].save_weights(f'dqn_model.h5')

        if isinstance(players[2], DqnAgent):
            players[2].save_weights(f'dqn_model.h5')


    def load_data(self, path):
        try:
            return json.load(open(path, "rb"))
        except:
            return {}

    def save_elo(self, players):

        file_names = os.listdir(self.FOLDER_PATH)

        for filename in file_names:
            data = json.load(fp=open(file=f'{os.path.abspath(os.path.join(self.FOLDER_PATH,filename))}',mode='r'))
            data[-1] = 10
            json.dump(fp=open(file=f'{os.path.abspath(os.path.join(self.FOLDER_PATH,filename))}',mode='w'))

        # for index in players:
        #     data = json.load(fp=open(file=f"..\\elo_ratings\\{players[index].player_name}.json", mode="r"))
        #     data[len(data)] = players[index].rating
        #     json.dump(obj=data, fp=open(file=f"..\\elo_ratings\\{players[index].player_name}.json",mode='w'))

