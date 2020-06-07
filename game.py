from players import QPlayer

class Game:
	def __init__(self,player1 , player2, rows=4,board=None, Q_learn=None, Q={}, alpha= 0.3, gamma= 0.9):
		self.player1 = player1
		self.player2 = player2
		self.current_player = player1
		self.other_player = player2
		self.board = board
		self.Q_learn = Q_learn
		self.Q_learn_or_not()


		if self.Q_learn:
			self.Q = Q
			self.alpha = alpha
			self.gamma = gamma

	def Q_learn_or_not(self):
		if self.Q_learn is None and (isinstance(self.player1, QPlayer) or isinstance(self.player2, QPlayer)):
			self.Q_learn = True

	def share_Q_with_players(self):
		if isinstance(self.player1, QPlayer):
			self.player1.Q = self.Q
		if isinstance(self.player2, QPlayer):
			self.player2.Q = self.Q

	def handle_move(self, move):

		if self.Q_learn:
			self.learn_Q()

		#act on the board with the given action "move"
		self.board.step(move)

		if self.board.is_terminal_state():
			self.declare_outcome()
		else:
			self.switch_players()

	def declare_outcome(self):
		print (f"the player {self.current_player} won the Game.")

	def switch_players(self):
		if self.current_player == self.player1:
			self.current_player = self.player2
			self.other_player = self.player1
		else:
			self.current_player = self.player1
			self.other_player = self.player2
		self.board.change_players()

	def reset(self):
		print("Reseting")
		self.board.reset()

	def learn_Q(self, move):
		pass

