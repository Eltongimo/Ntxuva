import numpy as np
import tkinter as tk

from board import Board
from players import Player, HumanPlayer, ComputerPlayer, RandomPlayer, THandPlayer, QPlayer

class Game:
    def __init__(self, master, player1, player2, Q_learn=None, Q={}, alpha=0.3, gamma=0.9):
        frame = tk.Frame()
        frame.grid()
        self.master = master
        master.title("ENPM808F - Robot Learning Tic Tac Toe")

        self.player1 = player1
        self.player2 = player2
        self.current_player = player1
        self.other_player = player2
        self.empty_text = ""
        self.board = Board()

        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        for i in range(3):
            for j in range(3):
                self.buttons[i][j] = tk.Button(frame, height=3, width=3, text=self.empty_text, command=lambda i=i, j=j: self.callback(self.buttons[i][j]))
                self.buttons[i][j].grid(row=i, column=j)

        self.reset_button = tk.Button(text="Reset", command=self.reset)
        self.reset_button.grid(row=3)

        self.Q_learn = Q_learn
        self.Q_learn_or_not()
        if self.Q_learn:
            self.Q = Q
            self.alpha = alpha          # Learning rate
            self.gamma = gamma          # Discount rate
            self.share_Q_with_players()

    def Q_learn_or_not(self):       # If either player is a QPlayer, turn on Q-learning
        if self.Q_learn is None:
            if isinstance(self.player1, QPlayer) or isinstance(self.player2, QPlayer):
                self.Q_learn = True

    def share_Q_with_players(self):             # The action value table Q is shared with the QPlayers to help them make their move decisions
        if isinstance(self.player1, QPlayer):
            self.player1.Q = self.Q
        if isinstance(self.player2, QPlayer):
            self.player2.Q = self.Q

    def callback(self, button):
        if self.board.over():
            pass                # Do nothing if the game is already over
        else:
            if isinstance(self.current_player, HumanPlayer) and isinstance(self.other_player, HumanPlayer):
                if self.empty(button):
                    move = self.get_move(button)
                    self.handle_move(move)
            elif isinstance(self.current_player, HumanPlayer) and isinstance(self.other_player, ComputerPlayer):
                computer_player = self.other_player
                if self.empty(button):
                    human_move = self.get_move(button)
                    self.handle_move(human_move)
                    if not self.board.over():               # Trigger the computer's next move
                        computer_move = computer_player.get_move(self.board)
                        self.handle_move(computer_move)

    def empty(self, button):
        return button["text"] == self.empty_text

    def get_move(self, button):
        info = button.grid_info()
        move = (int(info["row"]), int(info["column"]))                # Get move coordinates from the button's metadata
        return move

    def handle_move(self, move):
        # try:

        if self.Q_learn:
            self.learn_Q(move)
        i, j = move         # Get row and column number of the corresponding button
        self.buttons[i][j].configure(text=self.current_player.mark)     # Change the label on the button to the current player's mark
        self.board.place_mark(move, self.current_player.mark)           # Update the board
        if self.board.over():
            self.declare_outcome()
        else:
            self.switch_players()

        # except:
            # print ("There was an error handling the move.")
            # pass        # This might occur if no moves are available and the game is already over

    def declare_outcome(self):
        if self.board.winner() is None:
            print ("Draw match")
        else:
            print ("The game is over. The player with mark %s won!" % self.current_player.mark)

    def reset(self):
        print ("Resetting...")
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].configure(text=self.empty_text)
        self.board = Board(grid=np.ones((3,3))*np.nan)
        self.current_player = self.player1
        self.other_player = self.player2
        # np.random.seed(seed=0)      # Set the random seed to zero to see the Q-learning 'in action' or for debugging purposes
        self.play()

    def switch_players(self):
        if self.current_player == self.player1:
            self.current_player = self.player2
            self.other_player = self.player1
        else:
            self.current_player = self.player1
            self.other_player = self.player2

    def play(self):
        if isinstance(self.player1, HumanPlayer) and isinstance(self.player2, HumanPlayer):
            pass        # For human vs. human, play relies on the callback from button presses
        elif isinstance(self.player1, HumanPlayer) and isinstance(self.player2, ComputerPlayer):
            pass
        elif isinstance(self.player1, ComputerPlayer) and isinstance(self.player2, HumanPlayer):
            first_computer_move = self.player1.get_move(self.board)      # If player 1 is a computer, it needs to be triggered to make the first move.
            self.handle_move(first_computer_move)
        elif isinstance(self.player1, ComputerPlayer) and isinstance(self.player2, ComputerPlayer):
            while not self.board.over():        # Make the two computer players play against each other without button presses
                self.play_turn()
                # move = self.current_player.get_move(self.board)
                # self.handle_move(move)

    def play_turn(self):
        move = self.current_player.get_move(self.board)
        self.handle_move(move)

    def learn_Q(self, move):                        # If Q-learning is toggled on, "learn_Q" should be called after receiving a move from an instance of Player and before implementing the move (using Board's "place_mark" method)
        state_key = QPlayer.make_and_maybe_add_key(self.board, self.current_player.mark, self.Q)
        next_board = self.board.get_next_board(move, self.current_player.mark)
        reward = next_board.give_reward()
        next_state_key = QPlayer.make_and_maybe_add_key(next_board, self.other_player.mark, self.Q)
        if next_board.over():
            expected = reward
        else:
            next_Qs = self.Q[next_state_key]             # The Q values represent the expected future reward for player X for each available move in the next state (after the move has been made)
            if self.current_player.mark == "X":
                expected = reward + (self.gamma * min(next_Qs.values()))        # If the current player is X, the next player is O, and the move with the minimum Q value should be chosen according to our "sign convention"
            elif self.current_player.mark == "O":
                expected = reward + (self.gamma * max(next_Qs.values()))        # If the current player is O, the next player is X, and the move with the maximum Q vlue should be chosen
        change = self.alpha * (expected - self.Q[state_key][move])
        self.Q[state_key][move] += change
