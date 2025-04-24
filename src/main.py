from Environment import Environment
from Agent import Agent

def main():
    # Train model
    snake = Environment()
    agent = Agent()

    epochs = 100

    for epoch in range(len(epochs)):
        state = snake.reset()
        done = False

        while not done:
            state = snake.get_state()
            action = agent.choose_action(state)
            # step
            
            # get next state
            # next_state = snake
            # reward
            # update q
            pass

if __name__ == '__main__':
    main()