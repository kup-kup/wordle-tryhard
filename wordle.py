import random
from collections import defaultdict
from dataclasses import dataclass

with open('valid_words.txt') as f:
    VALID_WORDS = f.read().splitlines()

with open('valid_answers.txt') as f:
    VALID_ANSWERS = f.read().splitlines()

# @dataclass()
class Constraints:
    correct_position: list[None | str] = [None]*5
    wrong_position: list[set] = [set()]*5
    missing: set = set()
    min_count: dict[str, int] = defaultdict(int)
    max_count: dict[str, int] = defaultdict(int)

def get_incremental_constraints(consts: Constraints, step_consts: Constraints) -> Constraints:
    incremental_consts = Constraints()
    word_length = len(consts.correct_position)
    assert word_length == len(step_consts.wrong_position)

    # handle green
    for i in range(word_length):
        if not consts.correct_position[i] and step_consts.correct_position[i]:
            incremental_consts.correct_position[i] = step_consts.correct_position[i]
    
    # handle yellow
    for i in range(word_length):
        if not step_consts.wrong_position[i]:
            continue
        for step_yellow in step_consts.wrong_position[i]:
            if step_yellow not in consts.wrong_position[i]:
                incremental_consts.wrong_position[i].add(step_yellow)

    # handle gray
    incremental_consts.missing = step_consts.missing - consts.missing

    # handle count
    for k, v in step_consts.min_count.items():
        if consts.min_count[k] < v:
            incremental_consts.min_count[k] = v
    
    for k, v in step_consts.max_count.items():
        if consts.max_count.get(k, float('inf')) > v:
            incremental_consts.max_count[k] = v

    return incremental_consts

class Wordle:

    def __init__(
            self, 
            answer = None,
            turns = 6, 
        ):
        
        self.turns = turns
        self.feedback = []
        self.guesses = []
        self.word_length = 5 # no support for other lengths for now
        assert answer is None or len(answer) == 5

        # initialize answer
        if answer is None:
            self.answer = random.choice(VALID_ANSWERS)
        else:
            self.answer = answer

    def add_guess(self, guess):
        assert len(guess) == self.word_length

        self.guesses.append(guess)
        taken = [False] * self.word_length # specify which letters are used up for count constraint
        new_feedback = ['black'] * self.word_length

        for i in range(self.word_length):

            # handle green
            if guess[i] == self.answer[i]:
                new_feedback[i] = 'green'
                taken[i] = True
                continue
        
            # handle yellow
            for j in range(self.word_length): # loop answer
                if guess[i] == self.answer[j] and not taken[j]:
                    new_feedback[i] = 'yellow'
                    taken[j] = True

        self.feedback.append(new_feedback)
        return new_feedback

if __name__ == "__main__":
    wordle = Wordle(answer='later')
    feedback = wordle.add_guess('troll')
    print(feedback)
    