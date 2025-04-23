from tools import column
import random

class Interpreter:
    def __init__(self, environment, snake):
        self.environment = environment
        self.snake = snake
        self.snake_head = snake[0]

    def get_state(self, environment, snake_head, node_size=40):
        head_x, head_y = [(e//node_size)+1 for e in snake_head]
        state_vector = [column(environment[:head_y], head_x) +
                        environment[head_y][head_x+1:] +
                        column(environment[head_y+1:], head_x) +
                        environment[head_y][:head_x]]
        return state_vector

    def get_reward(self):
        pass
