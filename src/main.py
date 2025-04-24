from Environment import Environment
from Agent import Agent

def main():
    # Train model
    env = Environment()
    agent = Agent()

    epochs = 1000

    for epoch in range(len(epochs)):
        snake, apple = env.reset()
        state = env.get_state()
        done = False
        score = 0

        while not done:
            action = agent.choose_action(state)
            new_snake, new_head, is_dead, got_apple = env.step(action)
            if got_apple:
                # generate new apple (new_snake)
                pass
            next_state = env.get_state(new_snake)
            reward = env.get_reward(snake[0], new_head, apple, is_dead)
            agent.update_q_value(state, action, reward, next_state)

            state = next_state
            snake = new_snake
            done = is_dead
            if got_apple:
                score += 1
        epsilon = max(agent.min_epsilon, epsilon * agent.epsilon_decay)
        print(f"Épisode {epoch+1}, score : {score}, epsilon : {epsilon:.3f}")

if __name__ == '__main__':
    main()
