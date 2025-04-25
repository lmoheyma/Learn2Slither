# Snake AI using Reinforcement Learning (Q-Learning)

## I - Environment

The environment of the snake is represented by the board. The following rules apply to the board:

 - Board size: 10 cells by 10 cells.
 - Two green apples, in a random cell of the board.
 - One red apple, in a random cell of the board.
 - The snake starts with a length of 3 cells, also placed randomly and contiguously on the board.
 - If the snake hits a wall: Game over, this training session ends.
 - If the snake collides with its own tail: Game over, this training session ends.
 - The snake eats a green apple: snake’s length increase by 1. A new green apple appears on the board.
 - The snake eats a red apple: snake’s length decrease by 1. A new red apple appears on the board.
 - If the snake’s length drops to 0: Game over, this training session ends

## II - State

Snake vision: Your snake can only see in the 4 directions from its head. The following figure represents the terminal output that your program will compute, before asking the agent where the snake should move to. This output is matching the board representation from the previous figure.

## III - 