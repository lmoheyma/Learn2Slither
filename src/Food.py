import random
from dataclasses import dataclass

@dataclass
class Food:
    def __init__(self, width, height, behavior='good'):
        self.x = random.randint(0, width)
        self.y = random.randint(0, height)
        self.behavior = behavior
