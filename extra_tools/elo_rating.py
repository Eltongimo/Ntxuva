import math
import json


class EloRater:

    def __init__(self):
        pass

    def calculate_probability(self, ra, rb):
        return 1 / (1 + pow(10, (ra -rb)/400))

    #ra and rb are is the rating of players
    #k is an constant added to perform new elo rating calculations
    # d is the result of game that can assume 3 values  {0 1 2}
    #   0 - is is draw
    #   1 - if player1 won
    #   2 - if player2 won

    def new_rating(self, ra, rb, d,K=40):

        pa = self.calculate_probability(ra,rb)
        pb = self.calculate_probability(rb,ra)

        if d == 1:
            ra = ra + K * (1 - pa)
            rb = rb + K * (0 - pb)
        elif d == 2:
            ra = ra + K * (0 - pa)
            rb = rb + K * (1 - pb)
        else:
            ra = ra + K * (0.5 - pa)
            rb = rb + K * (0.5 - pb)
