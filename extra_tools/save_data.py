import json
# from agents.dqn.dqn import DqnAgent
class Save_data:

    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2
        self.dic = {

        }

    def save(self, players ):
        self.save_win_rate(player1_win=players[1].wins,player2_win=players[2].wins)
        self.save_models(players)

    def save_win_rate(self,player1_win, player2_win):
        with open(f"{self.filename}_win_rate_data.json", 'w') as f:
            json.dump({"player1": player1_win,
                       "player2": player2_win
                       }, f, indent=2)

    def save_models(self, players):
        pass
        # if isinstance(players[1], DqnAgent):
        #     players[1].save_weights(f'dqn_model.h5')
        #
        # if isinstance(players[2], DqnAgent):
        #     players[2].save_weights(f'dqn_model.h5')


    def load_data(self, path):
        try:
            return json.load(open(path, "rb"))
        except:
            return {}

    def get_elo(self,player_name):
        with open(file=f"../../elo_ratings/{player_name}.json", mode="r") as f1:
            data = json.load(f1)

            if len(data) == 0:
                return {"0": 1000}
            return data

    # players is an dictionary of players having keys 1 and 2
    def save_elo(self, filenames, data):
        for index in data:
            with open(file=f"../../elo_ratings/{filenames[index]}.json", mode="w") as file:
                json.dump(data[index],file, indent=2)
        print ("the new elo rating has been assigned to both players!")

