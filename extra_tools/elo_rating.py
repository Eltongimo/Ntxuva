class EloRater:

    def __init__(self, player1, player2, K=20):
        self.d = {player1: 1,
                  player2: 2,
                  None: 0}
        self.K =K

    def calculate_probability(self, ra, rb):
        return 1 / (1 + pow(10, (ra -rb)/400))

    #ra and rb are is the rating of players
    #k is an constant added to perform new elo rating calculations
    # d is the result of game that can assume 3 values  {0 1 2}
    #   0 - is is draw
    #   1 - if player1 won
    #   2 - if player2 won

    def new_rating(self, ra, rb, d):

        pa = self.calculate_probability(ra,rb)
        pb = self.calculate_probability(rb,ra)

        if d == 1:
            ra = ra + self.K * (1 - pa)
            rb = rb + self.K * (0 - pb)
        elif d == 2:
            ra = ra + self.K * (0 - pa)
            rb = rb + self.K * (1 - pb)
        else:
            ra = ra + self.K * (0.5 - pa)
            rb = rb + self.K * (0.5 - pb)

        return round(ra,2),round(rb,2)

