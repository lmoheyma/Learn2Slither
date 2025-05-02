import random
import numpy as np
import json
from tools import print_info
from colors import UGREEN, BHRED, RED, RESET
import os

class Agent:
    def __init__(self, epochs, save_file):
        self.Q_table = {}
        self.saved_table = {}
        self.learning_rate = 0.1
        self.epochs = epochs
        self.gamma = 0.99
        self.epsilon = 1
        self.min_epsilon = 0.01
        self.epsilon_decay = 0.95
        self.actions = [0, 1, 2, 3]
        self.scores_history = []
        self.movements = []
        self.save_file = save_file

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

    def save_q_table(self, filename='sess.json'):
        folder = '../models'
        try:
            if not os.path.isdir(folder):
                    os.mkdir(folder)
            with open(f'{folder}/{filename}', "w") as f:
                json.dump(self.saved_table, f, indent=4)
            print_info(f'Model saved in {UGREEN}{filename}')
        except Exception:
            print(f"{BHRED}Fail to save file '{RED}{filename}{BHRED}'.{RESET}")
            exit(1)

    def load_q_table(self, filename):
        try:
            print_info(f'Load trained model from {UGREEN}{filename}')
            with open(filename, 'r') as file:
                self.Q_table = json.load(file)
        except Exception:
            print(f"{BHRED}Fail to load file '{RED}{filename}{BHRED}'.{RESET}")
            exit(1)
