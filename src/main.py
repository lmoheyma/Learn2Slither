from Environment import Environment
from Agent import Agent
import tkinter as tk
from argparse import ArgumentParser

def main():
    parser = ArgumentParser(
        description='Learn2Slither')
    parser.add_argument('-sessions', type=int, default=1000,
                        help='Number of training sessions for the agent')
    parser.add_argument('-save', type=str,
                        help='Name of the model file to save')
    parser.add_argument('-visual', type=str,
                        choices=['on', 'off'],
                        default='on',
                        help="Visual mode: 'on' or 'off'")
    parser.add_argument('-load', type=str, default='../models/sess.json',
                        help='Path of the model to load')
    parser.add_argument('-dont-learn', action='store_true',
                        help='Agent will not learn')
    parser.add_argument('-step-by-step', type=str, default='../models/sess.json',
                        help='Path where the model will be save')

    args = parser.parse_args()
    
    root = tk.Tk()
    root.title("Snake AI")
    save_file = args.save
    if save_file is None:
        save_file = f'{args.sessions}sess.json'
    agent = Agent(args.sessions, save_file)
    Environment(root, agent=agent)
    root.mainloop()

if __name__ == '__main__':
    main()
