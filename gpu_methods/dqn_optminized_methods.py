import random
from numba import  njit
import numpy as np
from collections import deque


@njit
def replay(model,params,batch_size=64, memory =deque()):
    if len(memory) < batch_size:
        return

    mini_batch = random.sample(memory, batch_size)

    for state, action, reward, new_state, done in mini_batch:

        updated_value = reward

        if not done:
            updated_value = params['alpha'] * (reward + params['gamma'] * np.max(model.predict(new_state)[0]))

        q = model.predict(state)
        q[0][action] = updated_value

        model.fit(state, q, epochs=1, verbose=0)

        if params['EPSILON_MIN'] < params['EPSILON']:
            params['EPSILON'] *= params['EPSION_DECAY']
