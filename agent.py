import wordle
import random
import utils
from collections import defaultdict, Counter
from functools import lru_cache
import numpy as np

@lru_cache(None)
def _feedback_cached(guess: str, answer: str):
    return wordle.get_feedback(guess, answer)

class Agent:
    def __init__(self) -> None:
        pass

    def get_guess(self) -> str:
        return ''
    
    def recieve_feedback(self, status, feedback) -> None:
        return

class TerminalAgent(Agent):
    def get_guess(self) -> str:
        return input().strip()
    
    def recieve_feedback(self, status, feedback) -> None:
        print(f'{status = }')
        print(feedback)
        print()

class RandomAgent(Agent):
    """guess randomly from possible answers"""

    def __init__(self) -> None:
        self.possible_answers = wordle.VALID_ANSWERS
        self.last_guess = None

    def get_guess(self) -> str:
        self.last_guess = random.choice(self.possible_answers)
        return self.last_guess
    
    def recieve_feedback(self, status, feedback) -> None:
        assert self.last_guess is not None
        temp = []
        for word in self.possible_answers:
            if wordle.is_possible(self.last_guess, feedback, word):
                temp.append(word)

        self.possible_answers = temp

class InformationGainAgent(Agent):
    """maximizes information gain, minimizes expected possible words"""

    def __init__(self, seed=None) -> None:
        self.possible_answers = wordle.VALID_ANSWERS
        self.last_guess = None
        self.random = np.random.default_rng(seed)

    def get_guess(self, sample = 10) -> str:
        """sample answers, calculate possible words for each guess, 
        return guess with lowest possible words"""
        min_possible_count = float('inf')
        best_guesses = []

        sampled_answers = self.random.choice(self.possible_answers, size=min(sample, len(self.possible_answers)), replace=False)
        for guess in self.possible_answers:
            # partition current candidates by feedback for this guess
            partitions = Counter(_feedback_cached(guess, w) for w in self.possible_answers)
            # expected remaining size over sampled answers
            possible_count = sum(partitions[_feedback_cached(guess, ans)] for ans in sampled_answers)

            if possible_count < min_possible_count:
                min_possible_count = possible_count
                best_guesses = [guess]
            elif possible_count == min_possible_count:
                best_guesses.append(guess)
        
        self.last_guess = self.random.choice(best_guesses)
        return self.last_guess

    def recieve_feedback(self, status, feedback) -> None:
        assert self.last_guess is not None
        temp = []
        for word in self.possible_answers:
            if wordle.is_possible(self.last_guess, feedback, word):
                temp.append(word)

        self.possible_answers = temp

if __name__ == '__main__':
    with utils.TimePerf():
        agent = InformationGainAgent()
    # print(agent.feedback_matrix)