import random
import numpy as np
from collections import  deque
from keras.models import Sequential, load_model
from keras.layers import Dense
from agents.qplayerandothers.players import ComputerPlayer,RLAgent

class DqnAgent(ComputerPlayer,RLAgent):
    def __init__(self, mark,rating,state_size=32, action_size=16, alpha=0.95, gamma=0.998, memory_len= 2000):
        ComputerPlayer.__init__(self,mark=mark, rating=rating)
        RLAgent.__init__(self,alpha=alpha, gamma=gamma, EPSILON= 1, EPSILON_MIN=0.0001,
                         EPSILON_DECAY=0.9999, action_size=action_size)
        self.gamma = gamma
        self.state_size = state_size
        self.memory = deque(maxlen=memory_len)
        self.model = self.build_model(hidden_layers=1)
        self.player_name = "dqn"

    def build_model(self, hidden_layers,input_layer_activation='relu',
                    hidden_layer_activation='relu', output_layer_activation='linear',
                    ):

        model = Sequential()
        model.add(Dense(32, input_shape=(self.state_size,), activation=input_layer_activation))

        for layer in range(hidden_layers):
            model.add(Dense(32, activation=hidden_layer_activation))

        model.add(Dense(self.action_size, activation=output_layer_activation))
        model.compile(loss='mse', optimizer='adam')

        return model


    def act(self, state):
        if np.random.rand() > self.EPSILON:
            return self.positions[random.randrange(self.action_size)]
        predicted_values = self.model.predict(state)

        return self.positions[np.argmax(predicted_values[0])]


    def get_move(self, board):
        move = self.act(np.reshape(board.grid, [1, board.ROWS * board.COLUMNS]))
        return move

    def save_model(self):
        self.model.save(filepath=f"{self.player_name}.h5")

    def load_model(self, path):
        return load_model(filepath=path)

    def save_weights(self, path):
        self.model.save_weights(filepath=path)

    def load_weights(self, path):
        self.model.load_weights(filepath=path)

    def remember(self, state, action, reward, new_state, done):
        self.memory.append((state,action,reward,new_state,done))

    def replay(self, batch_size=32):

        if len(self.memory) < batch_size:
            return

        mini_batch = random.sample(self.memory, batch_size)

        for state, action, reward, new_state, done in mini_batch:

            updated_value = reward

            if not done:
                updated_value = self.alpha * (reward + self.gamma * np.max(self.model.predict(new_state)[0]))

            q = self.model.predict(state)
            q[0][action] = updated_value

            self.model.fit(state, q, epochs=1, verbose=0)

        if self.EPSILON_MIN < self.EPSILON:
            self.EPSILON *= self.EPSILON_DECAY


    def update_agent_policy(self,ntxuva, moved , action, captures ):
        board_copy = ntxuva.grid.copy()

        old_state_values = np.reshape(board_copy, [1, ntxuva.ROWS
                                                   * ntxuva.COLUMNS])

        new_state_values = np.reshape(board_copy, [1, ntxuva.ROWS
                                                   * ntxuva.COLUMNS])

        self.remember(state=old_state_values, action=action, new_state=new_state_values,
                        reward=round(captures / 10) if not ntxuva.over() else 1,
                        done=ntxuva.over())

        if not moved:
            self.replay(batch_size=32)


