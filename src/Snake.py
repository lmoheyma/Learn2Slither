import tkinter as tk
import random
from Food import Food
from tools import print_map

behavior_colors = {
    'good': 'green',
    'bad': 'red'
}

class Snake:
    def __init__(self, master, width=400, height=400,
                 nb_good_food=2, nb_bad_food=1):
        self.master = master
        self.width = width
        self.height = height
        self.node_size = 40
        self.canvas = tk.Canvas(master, width=width, height=height, bg='black')
        self.canvas.pack()
        self.snake = self.init_snake()
        self.foods = self.create_foods(nb_good_food, nb_bad_food)
        self.direction = 'Left'
        self.game_over = False

        master.bind('<Up>', lambda event: self.change_direction('Up'))
        master.bind('<Down>', lambda event: self.change_direction('Down'))
        master.bind('<Left>', lambda event: self.change_direction('Left'))
        master.bind('<Right>', lambda event: self.change_direction('Right'))

        self.update_map()
        self.game_loop()

    def update_map(self):
        self.map = [[0] * 12 for _ in range(12)]
        for i in range(len(self.map)):
            for j in range(len(self.map[i])):
                if i == 0 or i == len(self.map)-1 or\
                j == 0 or j == len(self.map[i])-1:
                    self.map[i][j] = 'W'
                for food in self.foods:
                    if food == [(j-1)*self.node_size, (i-1)*self.node_size]:
                        self.map[i][j] = food.tag
                for node in self.snake:
                    if node == [(j-1)*self.node_size, (i-1)*self.node_size]:
                        self.map[i][j] = 'H' if node == self.snake[0] else 'S'
        print_map(self.map)

    def init_snake(self):
        snake_head_x = random.randint(0, (self.width//self.node_size)-1) * self.node_size
        snake_head_y = random.randint(0, (self.width//self.node_size)-1) * self.node_size
        snake = [[snake_head_x, snake_head_y]]
        for _ in range(2):
            new_node = [snake[-1][0]+self.node_size, snake[-1][1]]
            snake.append(new_node)
        return snake

    def check_collision(self):
        if self.game_over: return
        if self.snake[0][0] > self.width or self.snake[0][0] < 0:
            self.game_over = True
        if self.snake[0][1] > self.height or self.snake[0][1] < 0:
            self.game_over = True
        for node in self.snake[1:]:
            if node == self.snake[0]:
                self.game_over = True

    def check_food(self):
        for food in self.foods:
            if self.snake[0] == food:
                self.foods.remove(food)
                self.canvas.delete(f'food{food.index}')
                if food.behavior == 'good':
                    self.append_node()
                else:
                    self.canvas.delete(self.snake[-1])
                    self.snake.pop()
                    if len(self.snake) < 1:
                        self.game_over= True
                        return
                self.foods.append(self.create_one_food(self.foods[-1].index+1, food.behavior))

    def create_one_food(self, index, behavior='good'):
        food = Food(self.width, self.height, self.node_size, index, behavior)
        self.canvas.create_rectangle(food.x, food.y, food.x+self.node_size,
                                     food.y+self.node_size, fill=behavior_colors[behavior],
                                     tags=f'food{index}')
        return food

    def create_foods(self, nb_good_food, nb_bad_food):
        foods = []
        i = 0
        for _ in range(nb_good_food): # Green food
            foods.append(self.create_one_food(index=i))
            i+=1
        for _ in range(nb_bad_food): # Red food
            foods.append(self.create_one_food(index=i, behavior='bad'))
            i+=1
        return foods

    def draw_snake(self):
        if self.game_over: return
        self.canvas.delete('snake')
        for node in self.snake:
            self.canvas.create_rectangle(node[0], node[1], node[0]+self.node_size, node[1]+self.node_size, fill='white', tags='snake')

    def append_node(self):
        if self.direction == 'Up':
            self.snake.append([self.snake[-1][0], self.snake[-1][1]+self.node_size])
        elif self.direction == 'Right':
            self.snake.append([self.snake[-1][0]-self.node_size, self.snake[-1][1]])
        elif self.direction == 'Down':
            self.snake.append([self.snake[-1][0], self.snake[-1][1]-self.node_size])
        elif self.direction == 'Left':
            self.snake.append([self.snake[-1][0]+self.node_size, self.snake[-1][1]])

    def move_snake(self):
        if self.game_over: return
        if self.direction == 'Up':
            self.snake.insert(0, [self.snake[0][0], self.snake[0][1]-self.node_size])
        elif self.direction == 'Right':
            self.snake.insert(0, [self.snake[0][0]+self.node_size, self.snake[0][1]])
        elif self.direction == 'Down':
            self.snake.insert(0, [self.snake[0][0], self.snake[0][1]+self.node_size])
        elif self.direction == 'Left':
            self.snake.insert(0, [self.snake[0][0]-self.node_size, self.snake[0][1]])
        self.canvas.delete(self.snake[-1])
        self.snake.pop()

    def change_direction(self, direction):
        if direction == 'Up' and self.direction != 'Down':
            self.direction = 'Up'
        elif direction == 'Right' and self.direction != 'Left':
            self.direction = 'Right'
        elif direction == 'Down' and self.direction != 'Up':
            self.direction = 'Down'
        elif direction == 'Left' and self.direction != 'Right':
            self.direction = 'Left'
        print(direction.upper())

    def game_loop(self):
        if not self.game_over:
            self.check_food()
            self.check_collision()
            self.draw_snake()
            self.move_snake()
            self.update_map()
            if not self.game_over:
                self.master.after(380, self.game_loop)
            else:
                self.canvas.create_text(200, 200, text="Game Over!", fill='white', font=('Helvetica', 30))


def main():
    root = tk.Tk()

    snake = Snake(root)
    root.mainloop()

if __name__ == '__main__':
    main()
