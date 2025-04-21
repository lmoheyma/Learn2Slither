import tkinter as tk
import random

class Snake:
    def __init__(self, master, width=400, height=400,
                 good_food=2, bad_food=2):
        self.master = master
        self.canvas = tk.Canvas(master, width=width, height=height, bg='black')
        self.canvas.pack()
        self.snake = self.init_snake(width, height)
        self.foods = self.create_food(good_food, bad_food)

    def init_snake(self, width, height):
        snake_head_x = random.randint(3, width-3)
        snake_head_y = random.randint(3, height-3)
        snake = [[snake_head_x, snake_head_y]]
        for i in range(2):
            new_node = [snake[-1][0]+1, snake[-1][1]]
            snake.append(new_node)
        return snake

    def check_collision(self):
        pass

    def create_food(self, good_food=True):
        pass

    def draw_snake(self):
        pass

    def move_snake(self):
        pass

    def change_direction(self, direction):
        pass


def main():
    root = tk.Tk()

    snake = Snake(root)
    root.mainloop()

if __name__ == '__main__':
    main()
