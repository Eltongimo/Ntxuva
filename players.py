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
            print("The player's mark must be either 'X' or 'O'.")


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
    def __init__(self, mark):
        super(RandomPlayer, self).__init__(mark=mark)
        self.mark = mark
        self.good_moves = 0
        self.bad_moves = 0

    def get_move(self, board):
        moves = board.available_moves(self.mark)
        if moves:  # If "moves" is not an empty list (as it would be if cat's game were reached)
            return moves[np.random.choice(
                len(moves))]  # Apply random selection to the index, as otherwise it will be seen as a 2D array


class QPlayer(ComputerPlayer):

    def __init__(self, mark, Q={}, alpha=0.1, gamma=0.88, action_space=16):
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


        if len(self.Q) > 0:
            print (f"Q table has been loaded len={len(self.Q)}")

    # state and new state are the key for each state transition
    def update_policy(self, state, new_state,new_state_qs, action, reward):
        # If the state is not found in the Q table, then we initialize that state  with random values of Q
        self.add_state(state)
        self.add_state(new_state)
        actions_q = self.Q[state]

        actions_q[action] = actions_q[action] + self.alpha * (reward + self.gamma * \
                                                              np.max(new_state_qs) - actions_q[action])
        self.Q[state] = [round(q,2) for q in actions_q]

    def add_state(self, state):
        if self.Q.get(state) is None:
            qs = np.random.random(size=(self.num_actions,))
            self.Q[state] = [round(q,2) for q in qs]


    def act(self, state):

        if np.random.rand() < self.EPSILON:
            return self.positions.get(np.random.randint(0, self.num_actions))

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

