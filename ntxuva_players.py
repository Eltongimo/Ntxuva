import numpy as np

class Player(object):
    def __init__(self, mark):
        self.mark = mark
        self.get_opponent_mark()

    def get_opponent_mark(self):
        if self.mark == 'X':
            self.opponent_mark = 'O'
        elif self.mark == 'O':
            self.opponent_mark = 'X'
        else:
            print ("The player's mark must be either 'X' or 'O'.")

class HumanPlayer(Player):
    pass

class ComputerPlayer(Player):

    def full_map_action_to_position(self, mark):
        q = {}
        if str(mark).upper() == 'O':
            action_num, first_row, second_row = 0, 2, 3
        elif str(mark).upper() == 'X':
            action_num, first_row, second_row = 0, 0, 1

        for i in [first_row, second_row]:
            for j in range(8):
                q[action_num] = (i, j)
                action_num += 1
        return q

class RandomPlayer(ComputerPlayer):
    @staticmethod
    def get_move(board):
        moves = board.available_moves(board.turn)
        if moves:   # If "moves" is not an empty list (as it would be if cat's game were reached)
            return moves[np.random.choice(len(moves))]    # Apply random selection to the index, as otherwise it will be seen as a 2D array

class THandPlayer(ComputerPlayer):
    def __init__(self, mark):
        super(THandPlayer, self).__init__(mark=mark)

    def get_move(self, board):
        moves = board.available_moves()
        if moves:
            for move in moves:
                if THandPlayer.next_move_winner(board, move, self.mark):
                    return move
                elif THandPlayer.next_move_winner(board, move, self.opponent_mark):
                    return move
            else:
                return RandomPlayer.get_move(board)

    @staticmethod
    def next_move_winner(board, move, mark):
        return board.get_next_board(move, mark).winner() == mark

# class QPlayer(ComputerPlayer):
#     def __init__(self, mark, Q={}, epsilon=0.2):
#         super(QPlayer, self).__init__(mark=mark)
#         self.Q = Q
#         self.epsilon = epsilon
#
#     def get_move(self, board):
#
#         if np.random.uniform() < self.epsilon:              # With probability epsilon, choose a move at random ("epsilon-greedy" exploration)
#             return RandomPlayer.get_move(board)
#         else:
#
#             state_key = QPlayer.make_and_maybe_add_key(board, self.mark, self.Q)
#             # print (state_key)
#             Qs = self.Q[state_key]
#
#             print("---- Vai imprimir o Qs ---------------")
#             print (Qs)
#
#             if self.mark == "X":
#                 # print (QPlayer.stochastic_argminmax(Qs, max))
#                 return QPlayer.stochastic_argminmax(board, Qs, max)
#             elif self.mark == "O":
#
#                 # print (QPlayer.stochastic_argminmax(Qs, min))
#                 return QPlayer.stochastic_argminmax(board, Qs, min)
#
#     @staticmethod
#     def make_and_maybe_add_key(board, mark, Q):     # Make a dictionary key for the current state (board + player turn) and if Q does not yet have it, add it to Q
#         default_Qvalue = 1.0       # Encourages exploration
#         state_key = board.make_key(mark)
#         if Q.get(state_key) is None:
#             moves = board.available_moves(board.turn)
#             Q[state_key] = {move: default_Qvalue for move in moves}    # The available moves in each state are initially given a default value of zero
#         return state_key
#
#     @staticmethod
#     def stochastic_argminmax(board, Qs, min_or_max):       # Determines either the argmin or argmax of the array Qs such that if there are 'ties', one is chosen at random
#
#         # min_or_maxQ = min_or_max(Qs.values())
#
#         '''
#         if Qs.values().count(min_or_maxQ) > 1:      # If there is more than one move corresponding to the maximum Q-value, choose one at random
#             best_options = [move for move in Qs.keys() if Qs[move] == min_or_maxQ]
#             move = best_options[np.random.choice(len(best_options))]
#         else:
#         '''
#
#         if len(Qs) > 0:
#             move = min_or_max(Qs, key=Qs.get)
#             return move
#
#
#         moves = board.available_moves(board.turn)
#         print(moves, board.grid, board.turn)
#         if moves:  # If "moves" is not an empty list (as it would be if cat's game were reached)
#             random_move = moves[np.random.choice(len(moves))]
#             print(random_move)
#             return random_move  # Apply random selection to the index, as otherwise it will be seen as a 2D array



class QPlayer(ComputerPlayer):

    def __init__(self, mark, alpha=0.1, gamma=0.88, Q={}, action_space=16):
        super(QPlayer, self).__init__(mark=mark)
        self.Q = Q
        self.gamma = gamma
        self.alpha = alpha
        self.num_actions = action_space
        self.EPSILON = 1
        self.EPSILON_DECAY = .999999
        self.mark = mark
        self.positions = ComputerPlayer(mark).full_map_action_to_position(mark=mark)

        # this attributes is for statistical
        self.bad_moves  = 0
        self.good_moves = 0

    # state and new state are the key for each state transition
    def update_policy(self, state, new_state,new_state_qs, action, reward):
        # If the state is not found in the Q table, then we initialize that state  with random values of Q
        self.add_state(state)
        self.add_state(new_state)
        actions_q = self.Q[state]

        actions_q[action] = actions_q[action] + (self.alpha) * (reward + self.gamma * \
                                                              np.max(new_state_qs) - actions_q[action])
        actions_q = [round(value,2) for value in actions_q]
        print (actions_q)

        self.Q[state] = actions_q

    def add_state(self, state):
        if self.Q.get(state) is None:
            qs = np.random.random(size=(self.num_actions,))
            qs = [round(values,2) for values in qs]
            self.Q[state] = qs


    def act(self,state):
        # if np.random.rand() < self.EPSILON:
        #     return self.positions.get(np.random.randint(0, self.num_actions))

        self.add_state(state)
        max_profit_move = np.argmax(self.Q[state])

        return self.positions[max_profit_move]

    def get_move(self, board):
        state_key = board.make_key(self.mark)
        move = self.act(state_key)
        return move


    def max(self, state):
        if self.Q.get(state) == None:
            self.Q[state] = np.random.random((self.num_actions,))
        return np.argmax(self.Q.get(state))

    def decay_epsilon(self):
        self.EPSILON *= self.EPSILON_DECAY


    def tuple_to_num(self, move):

        start = 0 if self.mark == 'X' else 2
        finish = 2 if self.mark == 'X' else 4

        counter = 0
        while start < finish:
            for j in range(self.num_actions):
                if (start,j) == move:
                   return counter
                counter = counter + 1
            start = start + 1

