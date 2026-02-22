import wordle
import random
import utils
from collections import defaultdict

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

class InformationGainAgent(Agent):
    """maximizes information gain, minimizes expected possible words"""

    def __init__(self) -> None:
        self.possible_answers = wordle.VALID_ANSWERS
        self.feedback_matrix = self._get_feedback_matrix()
        self.last_guess = None
    
    def _get_feedback_matrix(self) -> dict:
        """create all possible feedback, takes ~10s"""
        res = defaultdict(defaultdict[str, str])
        n = len(self.possible_answers)
        for i in range(n):
            word1 = self.possible_answers[i]
            for j in range(i+1, n):
                word2 = self.possible_answers[j]
                res[word1][word2] = ''.join(wordle.get_feedback(word1, word2))
                res[word2][word1] = ''.join(wordle.get_feedback(word2, word1))
        return res

    def get_guess(self) -> str:
        min_possible_count = len(self.possible_answers)
        best_guesses = []

        for guess in self.possible_answers:
            curr_possible_count = 0

            for answer in self.possible_answers:
                feedback = ''.join(wordle.get_feedback(guess, answer))

                for word in self.possible_answers:
                    if wordle.is_possible(guess, feedback, word):
                        curr_possible_count += 1
            
            if curr_possible_count == min_possible_count:
                best_guesses.append(guess)
            elif curr_possible_count < min_possible_count:
                best_guesses = [guess]
        
        self.last_guess = random.choice(best_guesses)
        return self.last_guess

    def recieve_feedback(self, status, feedback) -> None:
        temp = []
        for word in self.possible_answers:
            if wordle.is_possible(self.last_guess, feedback, word):
                temp.append(word)

        self.possible_answers = temp

if __name__ == '__main__':
    with utils.TimePerf():
        agent = InformationGainAgent()
    # print(agent.feedback_matrix)