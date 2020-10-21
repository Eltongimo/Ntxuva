import numpy as np
import pickle

class RLAgent:
    def __init__(self, alpha, gamma, EPSILON, EPSILON_DECAY, EPSILON_MIN, action_size):
        self.alpha = alpha
        self.gamma = gamma
        self.EPSILON = EPSILON
        self.EPSILON_DECAY = EPSILON_DECAY
        self.EPSILON_MIN = EPSILON_MIN
        self.action_size = action_size

class ComputerPlayer:
    def __init__(self, mark):
        self.mark = mark
        self.positions = self.full_map_action_to_position(mark)
        self.wins = 0
        self.player_name = ''

    def update_agent_policy(self,ntxuva, moved , action, captures ):
        pass

    def save_model(self):
        pass

    def load_model(self):
        pass

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
        super().__init__(mark=mark)
        self.player_name = 'random'

    def get_move(self, board):
        moves = board.available_moves(self.mark)
        if moves:  # If "moves" is not an empty list (as it would be if cat's game were reached)
            return moves[np.random.choice(
                len(moves))]  # Apply random selection to the index, as otherwise it will be seen as a 2D array

class QPlayer(ComputerPlayer, RLAgent):
    def __init__(self, mark,alpha=0.1, gamma=0.88, Q={}, action_space=16):
        ComputerPlayer.__init__(self,mark=mark)
        RLAgent.__init__(self,alpha=alpha, gamma=gamma,EPSILON=1, EPSILON_DECAY=0.9999,
                         EPSILON_MIN=0.0001, action_size=action_space)
        self.Q = Q
        self.player_name = 'qplayer'

    # state and new state are the key for each state transition
    def update_policy(self, state, new_state,new_state_qs, action, reward):
        # If the state is not found in the Q table, then we initialize that state  with random values of Q
        self.add_state(state)
        self.add_state(new_state)
        actions_q = self.Q[state]


        actions_q[action] = actions_q[action] + (self.alpha) * (reward + self.gamma * \
                                                              np.max(new_state_qs) - actions_q[action])
        actions_q = [round(value,2) for value in actions_q]
        self.Q[state] = actions_q

    def add_state(self, state):
        if self.Q.get(state) is None:
            qs = np.random.random(size=(self.action_size,))
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
            self.Q[state] = np.random.random((self.action_size,))
        return np.argmax(self.Q.get(state))

    def decay_epsilon(self):
        self.EPSILON *= self.EPSILON_DECAY


    def update_agent_policy(self,ntxuva, moved , action, captures ):
        old_state = ntxuva.make_key()
        new_state_qs = ntxuva.get_new_state_qs(self.mark)
        new_state = ntxuva.make_key()

        if moved:
            self.update_policy(state=old_state, new_state=new_state, new_state_qs=new_state_qs,
                                 action=action,
                                 reward=round(captures / 10, 1) if not ntxuva.over() else 1)
        else:
            self.update_policy(state=old_state, new_state=new_state, new_state_qs=new_state_qs,
                                 action=action,
                                 reward=-1)

    def save_model(self):
        pickle.dump(self.Q,open(f"{self.player_name}.p","wb"))
        print ("Q table has been saved!")

    def load_model(self,filepath):
        return pickle.load(open(f"{filepath}",'rb'))
