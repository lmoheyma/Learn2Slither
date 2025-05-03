import tkinter as tk
import random
import copy
from Food import Food
from Agent import Agent
from tools import column, print_map, get_key
from colors import BCYAN, RESET, BWHITE

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
                 nb_good_food=2, nb_bad_food=1, dont_train=False,
                 agent=Agent, visual_mode='off', no_replay=False):
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
        self.agent = agent
        self.visual_mode = visual_mode
        self.no_replay = no_replay

        master.bind('<Up>', lambda event: self.change_direction('Up'))
        master.bind('<Down>', lambda event: self.change_direction('Down'))
        master.bind('<Left>', lambda event: self.change_direction('Left'))
        master.bind('<Right>', lambda event: self.change_direction('Right'))

        if not dont_train: self.train_loop()
        else:
            self.agent.epsilon = self.agent.min_epsilon
            snake, apples = self.reset()
            self.update_map(snake, apples)
            self.agent_loop(snake, apples)

    def update_map(self, snake, foods):
        self.map = [[0] * 12 for _ in range(12)]
        for i in range(len(self.map)):
            for j in range(len(self.map[i])):
                if i == 0 or i == len(self.map)-1 or\
                j == 0 or j == len(self.map[i])-1:
                    self.map[i][j] = 'W'
                for food in foods:
                    if food == [j, i]:
                        self.map[i][j] = food.tag
                for node in snake:
                    if node == [j, i]:
                        self.map[i][j] = 'H' if node == snake[0] else 'S'

    def get_reward(self, is_dead, apple):
        if apple:
            return 20 if apple.behavior == 'good' else -40
        if is_dead:
            return -50
        return -1

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
        if ((new_head in snake) or self.check_collision(new_head)):
            return snake, True, None

        for apple in apples:
            if apple == new_head:
                got_apple = apple
        if got_apple is None:
            new_snake.pop()
        if got_apple and got_apple.behavior != 'good':
            new_snake.pop()
        return new_snake, False, got_apple

    def get_state(self, snake):
        def check_collision(point, snake):
            x, y = point
            if x <= 0 or x > self.width//self.node_size or y <= 0 or y > self.height//self.node_size:
                return True
            if point in snake[1:]:
                return True
            return False
        head = snake[0]
        point_left = [head[0]-1, head[1]]
        point_right = [head[0]+1, head[1]]
        point_up = [head[0], head[1]-1]
        point_down = [head[0], head[1]+1]

        dir_left = snake[1][0] > head[0]
        dir_right = snake[1][0] < head[0]
        dir_up = snake[1][1] > head[1]
        dir_down = snake[1][1] < head[1]

        if dir_up:
            danger_up = check_collision(point_up, snake)
            danger_right = check_collision(point_right, snake)
            danger_left = check_collision(point_left, snake)
            danger_down = True
        elif dir_down:
            danger_down = check_collision(point_down, snake)
            danger_right = check_collision(point_left, snake)
            danger_left = check_collision(point_right, snake)
            danger_up = True
        elif dir_left:
            danger_left = check_collision(point_left, snake)
            danger_up = check_collision(point_up, snake)
            danger_down = check_collision(point_down, snake)
            danger_right = True
        elif dir_right:
            danger_right = check_collision(point_right, snake)
            danger_down = check_collision(point_down, snake)
            danger_up = check_collision(point_up, snake)
            danger_left = True

        head_x, head_y = snake[0]
        collision_before_apple = False

        try:
            apple_up = head_y - column(self.map[:head_y], head_x).index('G')
            collision_before_apple = 'S' in column(self.map[abs(apple_up-head_y):head_y], head_x) and dir_up
            apple_up = 1
        except ValueError:
            apple_up = 0
        try:
            apple_right = self.map[head_y][head_x+1:].index('G')+1
            collision_before_apple = 'S' in self.map[head_y][head_x+1:head_x+apple_right+1] and dir_right
            apple_right = 1
        except ValueError:
            apple_right = 0
        try:
            apple_down = column(self.map[head_y+1:], head_x).index('G')+1
            collision_before_apple = 'S' in column(self.map[head_y+1:head_y+apple_down+1], head_x) and dir_down
            apple_down = 1
        except ValueError:
            apple_down = 0
        try:
            apple_left = head_x - self.map[head_y][:head_x].index('G')
            collision_before_apple = 'S' in self.map[head_y][abs(apple_left-head_x):head_x] and dir_left
            apple_left = 1
        except ValueError:
            apple_left = 0

        return [
            dir_left,
            dir_right,
            dir_up,
            dir_down,
            danger_up,
            danger_right,
            danger_down,
            danger_left,
            collision_before_apple,
            apple_up,
            apple_down,
            apple_left,
            apple_right
        ]

    def display_vision(self, snake):
        head_x, head_y = [e for e in snake[0]]
        self.vision_map = copy.deepcopy(self.map)
        for i in range(len(self.map)):
            for j in range(len(self.map[i])):
                if j != head_x and i != head_y:
                    self.vision_map[i][j] = ' '
                print(self.vision_map[i][j], end=' ')
            print()
        print()

    def init_snake(self):
        snake_head_x = random.randint(1, (self.width//self.node_size)-2) * self.node_size
        snake_head_y = random.randint(1, (self.width//self.node_size)) * self.node_size
        snake = [[snake_head_x, snake_head_y]]
        for _ in range(2):
            new_node = [snake[-1][0]+self.node_size, snake[-1][1]]
            snake.append(new_node)
        return [[(coord//self.node_size) for coord in node] for node in snake]

    def check_collision(self, snake_head):
        if snake_head[0] > self.width//self.node_size or snake_head[0] < 1:
            self.game_over = True
        if snake_head[1] > self.height//self.node_size or snake_head[1] < 1:
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

    def draw_snake(self, snake):
        self.canvas.delete('snake')
        for node in snake:
            if node == snake[0]: 
                self.canvas.create_rectangle(node[0], node[1], node[0]+self.node_size, node[1]+self.node_size, fill='purple2', tags='snake')
            else:
                self.canvas.create_rectangle(node[0], node[1], node[0]+self.node_size, node[1]+self.node_size, fill='MediumPurple2', tags='snake')

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

    def agent_loop(self, snake, apples):
        self.canvas.delete('food')
        for food in apples:
            x = (food.x-1) * self.node_size
            y = (food.y-1) * self.node_size
            self.canvas.create_rectangle(x, y, x+self.node_size,
                                    y+self.node_size, fill=behavior_colors[food.behavior],
                                    tags='food')
        self.draw_snake([[((coord-1)*self.node_size) for coord in node] for node in snake])
        state = self.get_state(snake)
        action = self.agent.choose_action(state)
        new_snake, is_dead, got_apple = self.step(action, snake, apples)
        self.update_map(new_snake, apples)
        if got_apple != None:
            apples.remove(got_apple)
            apples.append(self.create_one_food((apples[-1].index)+1, got_apple.behavior))
            if got_apple.behavior == 'good':
                self.agent.score+=1
                print(f'Score: {self.agent.score}')
        if not is_dead:
            self.master.after(280, lambda: self.agent_loop(new_snake, apples))
        else: self.canvas.create_text(200, 200, text="Game Over!", fill='white', font=('Helvetica', 30))

    def game_loop(self):
        if not self.game_over:
            self.check_food()
            self.draw_snake()
            self.move_snake()
            self.check_collision()
            self.update_map()
            if not self.game_over:
                self.display_vision()
                self.get_state(self.snake)
                self.master.after(380, self.game_loop)
            else:
                self.canvas.create_text(200, 200, text="Game Over!", fill='white', font=('Helvetica', 30))

    def replay_loop(self, action, index):
        snake = [[((coord-1)*self.node_size) for coord in node] for node in action[index]['snake']]
        self.canvas.delete('food')
        for food in action[index]['apples']:
            x = (food.x-1) * self.node_size
            y = (food.y-1) * self.node_size
            self.canvas.create_rectangle(x, y, x+self.node_size,
                                    y+self.node_size, fill=behavior_colors[food.behavior],
                                    tags='food')
        self.draw_snake(snake)
        if index < len(action)-1: self.master.after(280, lambda: self.replay_loop(action, index+1))
        else: self.canvas.create_text(200, 200, text="Game Over!", fill='white', font=('Helvetica', 30))

    def train_loop(self):
        for epoch in range(self.agent.epochs):
            i = 0
            snake, apples = self.reset()
            self.update_map(snake, apples)
            state = self.get_state(snake)
            done = False
            score = 0
            self.game_over = False
            game_states = []

            while not done:
                action = self.agent.choose_action(state)
                if self.visual_mode == 'on':
                    self.display_vision(snake)
                    print(get_key(direction, action).upper(), end='\n\n')
                new_snake, is_dead, got_apple = self.step(action, snake, apples)
                self.update_map(new_snake, apples)
                if got_apple != None:
                    apples.remove(got_apple)
                    apples.append(self.create_one_food((apples[-1].index)+1, got_apple.behavior))
                next_state = self.get_state(new_snake)
                reward = self.get_reward(is_dead, got_apple)
                self.agent.update_q_value(state, action, reward, next_state)

                state = next_state
                snake = new_snake
                game_states.append({
                    'snake': new_snake,
                    'apples': copy.deepcopy(apples)
                })
                done = is_dead
                if got_apple != None and got_apple.behavior == 'good':
                    score+=1
                i+=1
            self.agent.epsilon = max(self.agent.min_epsilon, self.agent.epsilon * self.agent.epsilon_decay)
            self.agent.scores_history.append({
                'score': score,
                'game_states': game_states,
            })
            print(f"Epoch {epoch+1}, score : {score}, epsilon : {self.agent.epsilon:.3f}, nb_iter : {i}")
        self.agent.scores_history = sorted(self.agent.scores_history, key=lambda x: x['score'])
        print(f'{BCYAN}Best score : {BWHITE}{self.agent.scores_history[-1]["score"]}{RESET}')
        self.agent.save_q_table(f'{self.agent.save_file}')
        if not self.no_replay: self.master.after(380, lambda: self.replay_loop(self.agent.scores_history[-1]["game_states"], 0))
