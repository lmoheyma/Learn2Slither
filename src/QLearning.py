from tools import column

class QLearning:
    def __init__(self):
        pass

def get_state(environment, snake_head, node_size=40):
    head_x, head_y = [(e//node_size)+1 for e in snake_head]
    state_vector = [column(environment[:head_y], head_x) +
                    environment[head_y][head_x+1:] +
                    column(environment[head_y+1:], head_x) +
                    environment[head_y][:head_x]]
    return state_vector
