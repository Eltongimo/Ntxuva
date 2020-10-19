import numpy as np
from scipy.optimize import linprog
from agents.qplayerandothers.players import ComputerPlayer

class MinimaxQPlayer(ComputerPlayer):
    def __init__(self, mark, numActionsA=16, numActionsB=16, decay=0.999, expl=1, gamma=0.9):
        super(MinimaxQPlayer, self).__init__(mark=mark)
        self.decay = decay
        self.expl = expl
        self.gamma = gamma
        self.alpha = 1
        self.V = {}
        self.Q = {}
        self.pi = {}
        self.numActionsA = numActionsA
        self.numActionsB = numActionsB
        self.learning = True
        self.mark = mark
        self.good_moves = 0
        self.bad_moves = 0
        self.positions = ComputerPlayer(mark).full_map_action_to_position(mark=mark)

    def chooseAction(self, state, restrict=None):
        self.get_state_values(state)
        if self.learning and np.random.rand() < self.expl:
            action = np.random.randint(self.numActionsA)
        else:
            action = self.weightedActionChoice(state)
        return action

    def get_state_values(self, state):
        if self.Q.get(state) is None:
            self.Q[state] = np.ones((self.numActionsA, self.numActionsA))
            self.V[state] = np.ones((self.numActionsA,))
            self.pi[state] = np.ones((1, self.numActionsA)) / self.numActionsA

    def weightedActionChoice(self, state):

        # if this state don't exists on the V, Q and pi table the add new row into these tables
        self.get_state_values(state)

        rand = np.random.rand()
        cumSumProb = np.cumsum(self.pi[state])
        action = 0
        while rand > cumSumProb[action]:
            action += 1
        return action

    def train(self, initialState, finalState, actions, reward, restrictActions=None):
        if not self.learning:
            return None

        self.get_state_values(initialState)
        self.get_state_values(finalState)

        actionA, actionB = actions
        q_value = self.Q.get(initialState)

        q_value[(actionA,actionB)] = (1 - self.alpha) * q_value[(actionA,actionB)] + self.alpha * (reward + self.gamma *max(self.V[finalState]))

        V = self.V[initialState]
        V[actionA] = min(np.sum(self.Q[initialState].T * self.pi[initialState], axis=1))
        self.alpha *= self.decay

    def updatePolicy(self, state, retry=False):
        c = np.zeros(self.numActionsA + 1)
        c[0] = -1
        A_ub = np.ones((self.numActionsB, self.numActionsA + 1))
        A_ub[:, 1:] = -self.Q[state].T
        b_ub = np.zeros(self.numActionsB)
        A_eq = np.ones((1, self.numActionsA + 1))
        A_eq[0, 0] = 0
        A_eq[0, 0] = 0
        b_eq = [1]
        bounds = ((None, None),) + ((0, 1),) * self.numActionsA

        res = linprog(c, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq, bounds=bounds)

        if res.success:
            self.pi[state] = res.x[1:]
        elif not retry:
            return self.updatePolicy(state, retry=True)
        else:
            print("Alert : %s" % res.message)
            return self.V[state]

        return np.random.random((self.numActionsA,)) / res.x[0]

    def get_move(self, board):
        state_key = board.make_key(self.mark)
        move = self.chooseAction(state_key)
        return self.positions.get(move)


