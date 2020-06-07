import numpy as np

class Player:
	def __init__(self):
		self.human = 'o'
		self.computer = 'x'
		
class ComputerPlayer(Player):
	pass

class HumanPlayer(Player):
	pass

class RandomPlayer(ComputerPlayer):
	def __init__(self, row1, row2 ):
		self.row1 = row1
		self.row2 = row2

	def get_move(self,env):
		moves = env.available_moves((self.row1,self.row2))
		choice = np.random.randint(low=0,high=len(moves))
		return moves[choice]

class QPlayer(ComputerPlayer):
		def __init__(self,alpha,gamma,epsilon,Q,action_space):
			self.Q = Q
			self.gamma = gamma
			self.alpha = alpha
			self.epsilon = epsilon
			self.epsilon_decay = 0.99
			self.num_actions = action_space
			self.EPSILON = 1
			self.EPSILON_DECAY = .999999

		def update_policy(self, state, new_state, action, reward):
				# If the state is not found in the Q table, then we initialize it with random values of Q
				self.add_new_state(state)

				actions_q = self.Q[state]

				if type(actions_q) == np.float64:
					actions_q = np.random.random(size=(self.num_actions))

				actions_q = actions_q[action] + self.alpha * (reward + self.gamma * (
					0.5 if self.Q.get(new_state) is None else np.max(self.Q[new_state])) - actions_q[action])
				self.Q[state] = actions_q


		def act(self, state):
			if np.random.rand() < self.EPSILON:
				return np.random.randint(0, self.num_actions)
			if self.Q.get(state) is None:
				self.add_new_state(state)
			return np.argmax(self.Q.get(state))

		def add_new_state(self, state):
			if self.Q.get(state) == None:
				self.Q[state] = np.random.random(size=(self.num_actions,))


		def max(self, state ):
			if self.Q.get(state) is None:
				self.Q[state] = np.random.random((self.num_actions))
			return np.argmax(self.Q.get(state))


		def decay_epsilon(self):
			self.EPSILON *= self.EPSILON_DECAY

class MoveConverter:

	def __init__(self, rows=4, columns=8):
		self.COLUMNS = columns
		self.ROWS = rows
		self.player1_actions, self.player2_actions = self.convert_moves()

	def convert_moves(self):
		player1_actions = {}
		counter = 0
		for i in [0, 1]:
			for j in range(self.COLUMNS):
				player1_actions[counter] = (i, j)
				counter += 1

		player2_actions = {}
		for i in [2, 3]:
			for j in range(self.COLUMNS):
				player2_actions[counter] = (i, j)
				counter += 1
		return player1_actions, player2_actions

