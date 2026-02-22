import wordle
import random

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
        temp = []
        for word in self.possible_answers:
            if wordle.is_possible(self.last_guess, feedback, word):
                temp.append(word)

        self.possible_answers = temp