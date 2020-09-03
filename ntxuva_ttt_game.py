import tkinter as tk
import numpy as np
import copy
from ntxuva_board import Ntxuva
from players import ComputerPlayer, QPlayer, RandomPlayer, HumanPlayer
from dqn import DqnAgent
from minimax import Minimax

class NtxuvaGame:
    def __init__(self, master, player1, player2, Q_learn=None, Q={}, alpha=0.3, gamma=0.9):
        frame = tk.Frame()
        frame.grid()
        self.master = master
        master.title("ENPM808F - Robot Learning Ntxtuva")

        self.player1 = player1
        self.player2 = player2
        self.current_player = player1
        self.other_player = player2
        self.empty_text = ""
        self.positions_x, self.positions_o = self.initialize_positions()
        self.ntxuva = Ntxuva(turn=self.current_player.mark)
        # self.ntxuva = Ntxuva(["0 0 0 0 0 0 0 1", "0 0 0 0 0 0 0 0", "1 0 0 0 0 0 0 0", "0 0 0 0 0 0 0 0"])
        # self.ntxuva = Ntxuva(["0 0 0 0 0 0 0 0", "0 0 0 0 1 0 0 0", "0 1 2 0 1 0 0 0", "0 0 0 1 0 1 0 0"])
        # self.ntxuva = Ntxuva(["0 1 2 0 0 0 1 0", "1 0 0 1 0 1 0 0", "0 1 0 1 0 0 1 1", "0 1 0 0 0 0 0 2"])
        # self.ntxuva = Ntxuva(["0 0 0 0 0 0 0 0", "0 0 0 0 0 1 0 0", "1 2 0 0 1 0 0 0", "0 1 0 1 0 0 1 0"])
        # self.ntxuva = Ntxuva(["1 0 1 0 1 0 1 1", "0 2 0 1 0 1 0 1", "1 0 1 0 1 0 1 0", "0 0 0 2 1 0 0 1"])
        # self.ntxuva = Ntxuva(["0 1 0 1 0 0 1 0", "1 0 1 0 1 0 2 1", "1 0 1 0 1 0 1 0", "0 0 2 0 1 1 0 1"])
        # self.ntxuva = Ntxuva(["0 0 1 1 3 0 0 0", "4 1 7 1 2 1 1 0", "0 1 0 1 0 1 0 1", "1 0 1 0 1 0 1 3"])

        self.buttons = [[None for _ in range(8)] for _ in range(4)]
        for i in range(4):
            for j in range(8):
                self.buttons[i][j] = tk.Button(frame, height=4, width=4, text=self.ntxuva.grid[(i, j)],
                                               command=lambda i=i, j=j: self.callback(self.buttons[i][j]))
                self.buttons[i][j].grid(row=i, column=j)

        self.reset_button = tk.Button(text="Reset", command=self.reset)
        self.reset_button.grid(row=4, column=8)

        self.Q_learn = Q_learn
        self.Q_learn_or_not()
        if self.Q_learn:
            self.Q = Q
            self.alpha = alpha  # Learning rate
            self.gamma = gamma  # Discount rate
            self.share_Q_with_players()

    def initialize_positions(self):
       pos_x = {}
       pos_o = {}
       counter = 0

       for i in range(4):
           if i == 2:
               counter = 0
           for j in range(8):
               if i < 2:
                   pos_x[(i,j)] = counter
               else:
                   pos_o[(i,j)] = counter
               counter = counter + 1
       return pos_x, pos_o

    def Q_learn_or_not(self):  # If either player is a QPlayer, turn on Q-learning
        if self.Q_learn is None:
            if isinstance(self.player1, QPlayer) or isinstance(self.player2, QPlayer):
                self.Q_learn = True

    def share_Q_with_players(self):  # The action value table Q is shared with the QPlayers to help them make their move decisions
        if isinstance(self.player1, QPlayer):
            self.player1.Q = self.Q
        if isinstance(self.player2, QPlayer):
            self.player2.Q = self.Q

    def callback(self, button):
        if self.ntxuva.over():
            pass
        else:
            if isinstance(self.current_player, HumanPlayer) and isinstance(self.other_player, HumanPlayer):
                move = self.get_move(button)
                if self.ntxuva.is_valid_move(move):
                    self.handle_move(move)
                else:
                    print('Invalid move!')

            elif isinstance(self.current_player, HumanPlayer) and isinstance(self.other_player, ComputerPlayer):
                computer_player = self.other_player
                move = self.get_move(button)

                valid_move = True
                if self.ntxuva.is_valid_move(move):
                    self.handle_move(move)
                else:
                    valid_move = False

                if not self.ntxuva.over() and valid_move:  # Trigger the computer's next move
                    while True:
                        computer_move = computer_player.get_move(self.ntxuva)
                        moved = self.handle_move(computer_move)

                        if moved:
                            break

            elif isinstance(self.current_player, HumanPlayer) and isinstance(self.other_player, RandomPlayer):
                random_player = self.other_player
                move = self.get_move(button)

                valid_move = True
                if self.ntxuva.is_valid_move(move):
                    self.handle_move(move)
                else:
                    print('Invalid move!')
                    valid_move = False

                if not self.ntxuva.over() and valid_move:  # Trigger the computer's next move
                    random_move = random_player.get_move(self.ntxuva)
                    self.handle_move(random_move)

    def handle_move(self, move):

        old_state = self.ntxuva.make_key(self.current_player.mark)

        # this values are stored to feed the ANN
        old_state_values = np.reshape(self.ntxuva.grid.copy(), [1, self.ntxuva.ROWS
                                                                        * self.ntxuva.COLUMNS])

        new_board, moved, captures = self.ntxuva.move(move)  # Update the board

        new_state = self.ntxuva.make_key(self.current_player.mark)

        new_state_values = np.reshape(self.ntxuva.grid.copy(), [1, self.ntxuva.ROWS
                                                                        * self.ntxuva.COLUMNS])

        # if the current player is the Q-learner then the policy must be optimized with the update_policy method using the Bellman's equation.
        if isinstance(self.current_player, QPlayer):
            new_state_qs = self.ntxuva.get_new_state_qs(self.current_player.mark)
            action = self.positions_x.get(move) if self.current_player.mark == 'X' else self.positions_o.get(move)

            if moved:
                self.current_player.update_policy(state=old_state, new_state=new_state, new_state_qs=new_state_qs,
                                                   action=action, reward=round(captures / 10, 1) if not self.ntxuva.over() else 1)
            else:
                self.current_player.update_policy(state=old_state, new_state=new_state, new_state_qs=new_state_qs,
                                                  action=action,
                                                  reward=-1)

        if isinstance(self.current_player, DqnAgent):
            action = self.positions_x.get(move) if self.current_player.mark == 'X' else self.positions_o.get(move)
            self.current_player.remember(state=old_state_values, action=action ,new_state=new_state_values,
                                         reward= round(captures / 10) if not self.ntxuva.over else 1 , done=self.ntxuva.over())

        if moved:
            for i in range(self.ntxuva.ROWS):
                for j in range(self.ntxuva.COLUMNS):
                    disable = True if (self.ntxuva.turn == 'X' and i < 2) or (
                                self.ntxuva.turn == 'O' and i > 1) else False
                    self.buttons[i][j].configure(text=self.ntxuva.grid[tuple((i, j))],
                                                 state=tk.DISABLED if disable else tk.NORMAL)  # Change the label on the button to the current player's mark

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
        else:
            pass 
        ''' 
            if isinstance(self.current_player,QPlayer):
                print("The game is over, qplayer won the game!")
            elif isinstance(self.current_player, RandomPlayer):
                print("The game is over, random player won the game!")
            elif isinstance(self.current_player, DqnAgent):
                print("The game is over, dqn player won the game!")
            elif isinstance(self.current_player, Minimax):
                print("The game is over, minimax player won the game!")
        '''
    def reset(self):
        self.ntxuva = Ntxuva()
        for i in range(self.ntxuva.ROWS):
            for j in range(self.ntxuva.COLUMNS):
                # disable = True if (self.ntxuva.turn == 'X' and i < 2) or (self.ntxuva.turn == 'O' and i > 1) else False
                self.buttons[i][j].configure(text=self.ntxuva.grid[tuple((i, j))], state=tk.NORMAL)
        self.current_player = self.player1
        self.other_player = self.player2

        if isinstance(self.player1, QPlayer) or isinstance(self.player1, DqnAgent):
            self.player1.bad_moves = 0
            self.player1.good_moves = 0

        if isinstance(self.player2, DqnAgent) or isinstance(self.player2, QPlayer):
            self.player2.bad_moves = 0
            self.player2.good_moves = 0

    def get_move(self, button):
        info = button.grid_info()
        move = (int(info["row"]), int(info["column"]))  # Get move coordinates from the 'buttons metadata
        return move


    def play(self):
        if isinstance(self.player1, HumanPlayer) and isinstance(self.player2, HumanPlayer):
            pass  # For human vs. human, play relies on the callback from button presses
        elif isinstance(self.player1, HumanPlayer) and isinstance(self.player2, ComputerPlayer):
            pass
        elif isinstance(self.player1, ComputerPlayer) and isinstance(self.player2, HumanPlayer):
            first_computer_move = self.player1.get_move(self.ntxuva)  # If player 1 is a computer, it needs to be triggered to make the first move.
            self.handle_move(first_computer_move)
        elif isinstance(self.player1, ComputerPlayer) and isinstance(self.player2, ComputerPlayer):
            while not self.ntxuva.over():  # Make the two computer players play against each other without button presses
                self.play_turn()
            return self.current_player
        
    def play_turn(self):
        move = self.current_player.get_move(self.ntxuva)

        if self.ntxuva.is_valid_move(move):

            self.current_player.good_moves = self.current_player.good_moves + 1
            self.handle_move(move)

        else:
            # gathering statistical data
            self.current_player.bad_moves = self.current_player.bad_moves + 1

            # the player has commited a wrong move
            if isinstance(self.current_player, QPlayer):
                state = self.ntxuva.make_key(self.current_player.mark)
                new_state_qs = self.ntxuva.get_new_state_qs(self.current_player.mark)
                action = self.positions_x.get(move) if self.current_player.mark == 'X' else self.positions_o.get(move)

                # penalizing tha agent for bad move....
                self.current_player.update_policy(state=state, new_state=state, new_state_qs=new_state_qs,
                                                  action=action, reward=-1)                
                
            if isinstance(self.current_player, DqnAgent):

                state = np.reshape(self.ntxuva.grid, [1, self.ntxuva.ROWS * self.ntxuva.COLUMNS])
                new_state = state
                action = self.positions_x.get(move) if self.current_player.mark == 'X' else self.positions_o.get(move)

                self.current_player.remember(state=state,action=action,new_state=new_state,
                                             reward=-1, done=False)
                self.current_player.replay()
                self.current_player.bad_moves = self.current_player.bad_moves + 1
