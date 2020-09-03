import random
import numpy as np
from collections import  deque
from keras.models import Sequential, load_model
from keras.layers import Dense
from keras.optimizers import  Adam
from players import ComputerPlayer


class DqnAgent(ComputerPlayer):

    def __init__(self, mark,state_size=32, action_size=16, alpha=0.95, gamma=0.998, memory_len= 2000, lr=0.001):
        super(DqnAgent, self).__init__(mark=mark)

        self.mark = mark

        self.EPSILON = 1
        self.EPSION_DECAY = 0.9999
        self.EPSILON_MIN = 0.0001

        self.ADAM_LR = lr

        self.state_size = state_size
        self.action_size = action_size

        self.alpha = alpha
        self.gamma = gamma

        self.memory = deque(maxlen=memory_len)

        self.model = self.build_model(hidden_layers=3)

        self.positions = ComputerPlayer(mark=self.mark).full_map_action_to_position(self.mark)

        self.good_moves = 0
        self.bad_moves = 0

    def build_model(self, hidden_layers= 2,input_layer_activation='relu',
                    hidden_layer_activation='relu', output_layer_activation='linear',
                    loss_function='mse'):

        model = Sequential()
        model.add(Dense(32, input_shape=(self.state_size,), activation=input_layer_activation))

        for layer in range(hidden_layers):
            model.add(Dense(32, activation=hidden_layer_activation))

        model.add(Dense(self.action_size, activation=output_layer_activation))
        model.compile(loss=loss_function, optimizer=Adam(lr=self.ADAM_LR))

        return model


    def act(self, state):
        if np.random.rand() > self.EPSILON:
            return self.positions[random.randrange(self.action_size)]
        predicted_values = self.model.predict(state)

        return self.positions[np.argmax(predicted_values[0])]


    def get_move(self, board):
        move = self.act(np.reshape(board.grid, [1, board.ROWS * board.COLUMNS]))
        return move

    def save_model(self, path):
        self.model.save(filepath=path)

    def load_model(self, path):
        return load_model(filepath=path)

    def save_weights(self, path):
        self.model.save_weights(filepath=path)

    def load_weights(self, path):
        self.model.load_weights(filepath=path)

    def remember(self, state, action, reward, new_state, done):
        self.memory.append((state,action,reward,new_state,done))

    def replay(self, batch_size=64):

        if len(self.memory) < batch_size:
            return

        mini_batch = random.sample(self.memory, batch_size)

        for state, action, reward, new_state, done in mini_batch:

            updated_value = reward

            if not done:
                updated_value = self.alpha * (reward + self.gamma * np.max(self.model.predict(new_state)[0]))

            q = self.model.predict(state)
            q[0][action] = updated_value

            self.model.fit(state,q, epochs=1, verbose=0)


            if self.EPSILON_MIN < self.EPSILON:
                self.EPSILON *= self.EPSION_DECAY
