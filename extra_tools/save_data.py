import json
import pickle

class Save_data:

    def __init__(self, player1, player2, filename):
        self.player1 = player1
        self.player2 = player2
        self.filename = filename

    def save(self, players, ratings):
        self.save_win_rate(player1_win=players[1].wins,player2_win=players[2].wins)
        self.save_models(players)
        self.save_elo(filenames={1: players[1].player_name, 2: players[1].player_name}, data=ratings)

    def save_win_rate(self,player1_win, player2_win):
        with open(f"{self.filename}.json", 'w') as f:
            json.dump({f"{self.player1.player_name}": player1_win,
                       f"{self.player2.player_name}": player2_win
                       }, f, indent=2)

    def save_models(self, players):
        for index in players:
            pickle.dump(players[index], open(f"{players[index].player_name}.p","wb"))

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

