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
                        default='off',
                        help="Visual mode: 'on' or 'off'")
    parser.add_argument('-load', type=str,
                        help='Path of the model to load')
    parser.add_argument('-dont-learn', action='store_true',
                        help='Agent will not learn')
    parser.add_argument('-no-replay', action='store_true',
                        help='No replay of the best game during training sessions')
    parser.add_argument('-display-speed', type=int, default=30,
                        help='Time in miliseconds between step during training phase')
    parser.add_argument('-step-by-step', action='store_true',
                        help='Auto-configuration of a human readable speed')

    args = parser.parse_args()
    
    root = tk.Tk()
    root.title("Snake AI")
    save_file = args.save
    if save_file is None:
        save_file = f'{args.sessions}sess.json'
    agent = Agent(args.sessions, save_file)
    if args.load is not None: agent.load_q_table(args.load)
    Environment(root, agent=agent,
    dont_train=args.dont_learn,
                visual_mode=args.visual,
                no_replay=args.no_replay,
                display_speed=args.display_speed,
                step_by_step=args.step_by_step)
    if not args.no_replay or args.visual == 'on': root.mainloop()

if __name__ == '__main__':
    main()
