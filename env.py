from wordle import Wordle
from agent import Agent

class Env:
    def __init__(self, instance: Wordle, agent: Agent):
        self.instance = instance
        self.agent = agent
    
    def play(self, verbose = False):
        status = 'playing'
        while status == 'playing':
            guess = self.agent.get_guess()
            status, feedback = self.instance.add_guess(guess)
            self.agent.recieve_feedback(status, feedback)

            if verbose:
                print(f'turn: {self.instance.turn}, status: {status}, guess: {guess}, feedback: {feedback}')