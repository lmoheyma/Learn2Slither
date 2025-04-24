from tools import column
import random

class Interpreter:
    def __init__(self, environment, snake):
        self.environment = environment
        self.snake = snake
        self.snake_head = snake[0]

    

    def get_reward(self):
        pass
