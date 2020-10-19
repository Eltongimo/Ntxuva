from game.ntxuva_board import Ntxuva
from gpu_methods import optimized_methods

class NtxuvaGame:
    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2
        self.current_player = player1
        self.other_player = player2
        self.counter = -1
        self.positions_x, self.positions_o = self.initialize_positions()
        self.ntxuva = Ntxuva(turn=self.current_player.mark)

    def increase_counter(self):
        self.counter = self.counter + 1
        return self.counter

    def initialize_positions(self):
        pos_x = {(i,j): self.increase_counter() for i in [0,1] for j in range(8)}
        self.counter = -1
        pos_o = {(i,j): self.increase_counter() for i in [2,3] for j in range(8)}
        return pos_x, pos_o

    def handle_move(self, move, action):

        new_board, moved, captures = optimized_methods.move(move, self.ntxuva.grid)  # Update the board
        self.current_player.update_agent_policy(self.ntxuva, moved , action, captures )

        if moved:
            if self.ntxuva.over():
                self.declare_outcome()
            else:
                self.switch_players()
        return moved

    def switch_players(self):
        if self.current_player == self.player1:
            self.current_player = self.player2
            self.other_player = self.player1
        else:
            self.current_player = self.player1
            self.other_player = self.player2
        self.ntxuva.change_turn()

    def declare_outcome(self):
        if self.ntxuva.winner() is None:
            print("Draw match")
            self.current_player = None


    def reset(self):
        self.ntxuva = Ntxuva()
        self.current_player = self.player1
        self.other_player = self.player2


    def play(self):
        while not self.ntxuva.over():  # Make the two computer players play against each other without button presses
            self.play_turn()
        return self.current_player

    def play_turn(self):
        move = self.current_player.get_move(self.ntxuva)
        action = self.positions_x.get(move) if self.current_player.mark == 'X' else self.positions_o.get(move)

        if self.ntxuva.is_valid_move(move):
            self.handle_move(move, action)
        else:
            self.current_player.update_agent_policy(ntxuva=self.ntxuva, moved=False,action=action,  captures=0)
