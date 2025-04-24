import random
import numpy as np

class Agent:
    def __init__(self):
        self.q_table = {}
        self.learning_rate = 0.1
        self.discount_factor = 0.99
        self.exploration_rate = 0.9

    def choose_action(self, state):
        if random.uniform(0, 1) < self.exploration_rate:
            return random.randint(0, 3)
        else:
            return np.argmax(self.q_table[state])
        
    def update_q_value(self, state, action, reward, next_state):
        max_future_q = np.max(self.q_table[next_state])
        current_q = self.q_table[state][action]
        self.q_table[state][action] = current_q + self.learning_rate * \
            (reward + self.discount_factor * max_future_q - current_q)
