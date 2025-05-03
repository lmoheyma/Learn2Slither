import random
from dataclasses import dataclass

food_tags = {
    'good': 'G',
    'bad': 'R'
}


@dataclass
class Food:
    def __init__(self, width, height, node_size, index, behavior='good'):
        self.index = index
        self.x = random.randint(1, (width//node_size)-1) * node_size
        self.y = random.randint(1, (height//node_size)-1) * node_size
        self.behavior = behavior
        self.tag = food_tags[behavior]
        self.node_size = node_size

    def __eq__(self, other):
        if isinstance(other, (list, tuple)) and len(other) == 2:
            return self.x == other[0] and self.y == other[1]
        return False

    def __repr__(self):
        return repr(f"{[self.x, self.y]}")
