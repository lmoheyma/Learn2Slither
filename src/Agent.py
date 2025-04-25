import random
import numpy as np

class Agent:
    def __init__(self):
        self.Q_table = {}
        self.learning_rate = 0.1
        self.gamma = 0.99
        self.epsilon = 1
        self.min_epsilon = 0.01
        self.epsilon_decay = 0.995
        self.actions = [0, 1, 2, 3]

    def choose_action(self, state):
        state_str = str(state)
        if random.random() < self.epsilon or state_str not in self.Q_table:
            return random.randint(0, 3)
        else:
            return np.argmax(self.Q_table[state_str])

    def update_q_value(self, state, action, reward, next_state):
        state_str = str(state)
        next_state_str = str(next_state)

        if state_str not in self.Q_table:
            self.Q_table[state_str] = [0.0 for _ in self.actions]
        if next_state_str not in self.Q_table:
            self.Q_table[next_state_str] = [0.0 for _ in self.actions]

        best_next = max(self.Q_table[next_state_str])
        self.Q_table[state_str][action] += self.learning_rate * (reward + self.gamma * best_next - self.Q_table[state_str][action])
