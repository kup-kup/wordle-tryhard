import random
from collections import defaultdict

class Wordle:

    def __init__(
            self, 
            init_guesses = None, 
            answer = None,
            turns = 6, 
        ):
        
        self.turns = turns
        self.feedback = []
        self.guesses = init_guesses if init_guesses else []
        self.word_length = 5 # no support for other lengths for now
        assert answer is None or len(answer) == 5

        # self.word_length = len(answer) if answer else 5 
        # word_length needs to be 5 if no answer is provided
        # as the class randomizes answers from 5 letters word list
        
        self.constraints = self._get_constraint_holder()

        # initialize valid words
        with open('valid_words.txt') as f:
            self.valid_words = f.read().splitlines()
        
        # initialize valid answers and possible answers
        with open('valid_answers.txt') as f:
            self.valid_answers = f.read().splitlines()
        self.possible_answers = set(self.valid_answers)

        # initialize answer
        if answer is None:
            self.answer = random.choice(self.valid_answers)
        else:
            self.answer = answer
        
        # initialize letter_index
        self.letter_index = defaultdict(list)
        for i in range(self.word_length):
            self.letter_index[self.answer[i]].append(i)

        for guess in self.guesses:
            self.add_guess(guess)

    def _get_constraint_holder(self):
        return {
            'green': [None] * self.word_length,
            'yellow': [set() for _ in range(self.word_length)],
            'gray': set(), # represents letters not present in answer as it is easier to handle
            # In normal wordle, gray can includes letters that exist in a word
            # but that slot is taken by another letter in the guessing word. 
            # For example, for the answer "later" and guess "troll". The first 
            # "l" in "troll" would be yellow but the second one would be gray,
            # even though the answer has "l" in it.

            'count': defaultdict(int) # letter -> min_count
        }
    
    def _get_incremental_constraints(self, step_constraints):
        incremental_constraintss = self._get_constraint_holder()

        # handle green
        for i in range(self.word_length):
            if not self.constraints['green'][i] and step_constraints['green'][i]:
                incremental_constraintss['green'][i] = step_constraints['green'][i]
        
        # handle yellow
        for i in range(self.word_length):
            if not step_constraints['yellow'][i]:
                continue
            for step_yellow in step_constraints['yellow'][i]:
                if step_yellow not in self.constraints['yellow'][i]:
                    incremental_constraintss['yellow'][i].add(step_yellow)

        # handle gray
        incremental_constraintss['gray'] = step_constraints['gray'] - self.constraints['gray']

        # handle count
        for k, v in step_constraints['count'].items():
            if self.constraints['count'][k] < v:
                incremental_constraintss['count'][k] = v

        return incremental_constraintss
    
    def _update_possible_answers(self, step_constraints):
        incremental_constraints = self._get_incremental_constraints(step_constraints)
        raise NotImplementedError()

    def add_guess(self, guess):
        assert len(guess) == self.word_length
        if guess not in self.valid_words:
            print("Invalid guess")
            return

        self.guesses.append(guess)
        step_constraints = self._get_constraint_holder() # constraints specifically from this new guess
        taken = [False] * self.word_length # specify which letters are used up for count constraint

        # handle green
        for i in range(self.word_length):
            if guess[i] == self.answer[i]:
                step_constraints['green'][i] = guess[i]
                step_constraints['count'][guess[i]] += 1
                taken[i] = True
        
        # handle yellow
        for i in range(self.word_length):
            if (guess[i] != self.answer[i] and guess[i] in self.letter_index):
                for j in self.letter_index[guess[i]]:
                    if taken[j]:
                        continue
                    step_constraints['yellow'][i].add(guess[i])
                    step_constraints['count'][guess[i]] += 1
                    taken[j] = True
                    break
        
        # handle gray
        for i in range(self.word_length):
            if guess[i] not in self.letter_index:
                step_constraints['gray'].add(guess[i])
        
        self._update_possible_answers(step_constraints)

if __name__ == "__main__":
    wordle = Wordle()
    print(len(wordle.valid_words))
    print(len(wordle.valid_answers))