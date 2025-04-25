import tkinter as tk
import random
import copy
from Food import Food
from Agent import Agent
from tools import column

behavior_colors = {
    'good': 'green',
    'bad': 'red'
}

direction = {
    'Up': 0,
    'Down': 1,
    'Left': 2,
    'Right': 3
}

class Environment:
    def __init__(self, master, width=400, height=400,
                 nb_good_food=2, nb_bad_food=1, train=False):
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
        if train: self.game_loop()
        else: self.train_loop()

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

    def get_reward(self, new_head, snake, apples):
        for apple in apples:
            if apple == new_head:
                if apple.behavior == 'good':
                    return 20
                return -20
            if (new_head in snake) or not (0 <= new_head[0] < self.width//self.node_size) or not (0 <= new_head[1] < self.height//self.node_size):
                return -50
        return -5

    def reset(self):
        snake = self.init_snake()
        apples = self.create_foods(2, 1)
        return snake, apples

    def step(self, action, snake, apples):
        head_x, head_y = snake[0]
        move = [(0, -1), (0, 1), (-1, 0), (1, 0)][action]
        new_head = [head_x + move[0], head_y + move[1]]
        got_apple = None

        new_snake = [new_head] + snake
        # if (self.check_collision(new_head, new_snake[:-1])):
        #     return new_snake, new_head, True, got_apple
        if (new_head in snake):
            print('EAT ITSELF')
        if (new_head in snake) or not (0 <= new_head[0] < self.width//self.node_size) or not (0 <= new_head[1] < self.height//self.node_size):
            print(new_head, new_snake)
            return snake, new_head, True, None

        # print(apples)
        for apple in apples:
            if apple == new_head:
                print('APPLEEEE')
                got_apple = apple
        if got_apple == None:
            new_snake.pop()
        if got_apple and got_apple.behavior != 'good':
            new_snake.pop()
        return new_snake, new_head, False, got_apple

    def get_next_state(self, action):
        self.change_direction(action)
        self.move_snake()
        return self.get_state()

    def get_state(self, snake, vision=3):
        head_x, head_y = snake[0]
        state_vector = [column(self.map[head_y-vision:head_y], head_x) +
                        self.map[head_y][head_x+1:head_x+vision+1] +
                        column(self.map[head_y+1:head_y+vision+1], head_x) +
                        self.map[head_y][head_x-vision:head_x]]
        return state_vector

    def display_vision(self):
        head_x, head_y = [(e//self.node_size)+1 for e in self.snake[0]]
        self.vision_map = copy.deepcopy(self.map)
        for i in range(len(self.map)):
            for j in range(len(self.map[i])):
                if j != head_x and i != head_y:
                    self.vision_map[i][j] = ' '
                print(self.vision_map[i][j], end=' ')
            print()
        print()

    def init_snake(self):
        snake_head_x = random.randint(0, (self.width//self.node_size)-1) * self.node_size
        snake_head_y = random.randint(0, (self.width//self.node_size)-1) * self.node_size
        snake = [[snake_head_x, snake_head_y]]
        for _ in range(2):
            new_node = [snake[-1][0]+self.node_size, snake[-1][1]]
            snake.append(new_node)
        return [[(coord//self.node_size) for coord in node] for node in snake]

    def check_collision(self, snake_head, snake):
        if snake_head[0] > self.width//self.node_size or snake_head[0] < 0:
            self.game_over = True
        if snake_head[1] > self.height//self.node_size or snake_head[1] < 0:
            self.game_over = True
        print(f'snake_head: {snake_head}')
        print(snake)
        for node in snake[1:]:
            if node == snake_head:
                print('EAT ITSELF')
                self.game_over = True
        return self.game_over

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
        food.x //=self.node_size
        food.y //=self.node_size
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
            self.draw_snake()
            self.move_snake()
            self.check_collision()
            self.update_map()
            # print_map(self.map)
            if not self.game_over:
                self.display_vision()
                self.get_state(self.snake)
                self.master.after(380, self.game_loop)
            else:
                self.canvas.create_text(200, 200, text="Game Over!", fill='white', font=('Helvetica', 30))

    def train_loop(self):
        agent = Agent()

        epochs = 1000

        for epoch in range(epochs):
            i = 0
            snake, apples = self.reset()
            state = self.get_state(snake)
            done = False
            score = 0
            self.game_over = False

            while not done:
                action = agent.choose_action(state)
                new_snake, new_head, is_dead, got_apple = self.step(action, snake, apples)
                if got_apple != None:
                    print('APPLE')
                    apples.remove(got_apple)
                    apples.append(self.create_one_food((apples[-1].index)+1, got_apple.behavior))
                    print(apples)
                next_state = self.get_state(new_snake)
                reward = self.get_reward(new_head, new_snake, apples)
                agent.update_q_value(state, action, reward, next_state)

                state = next_state
                snake = new_snake
                done = is_dead
                if got_apple != None:
                    score += 1
                i+=1
                print(new_head)
            agent.epsilon = max(agent.min_epsilon, agent.epsilon * agent.epsilon_decay)
            print(f"Epoch {epoch+1}, score : {score}, epsilon : {agent.epsilon:.3f}, nb_iter : {i}")

def main():
    root = tk.Tk()

    Environment(root)
    # root.mainloop()

if __name__ == '__main__':
    main()
