import random
from functools import lru_cache

with open('valid_words.txt') as f:
    VALID_WORDS = f.read().splitlines()

with open('valid_answers.txt') as f:
    VALID_ANSWERS = f.read().splitlines()

@lru_cache()
def is_possible(guess: str, feedback: str, word: str) -> bool:
    """check if the word is possible from feedback"""
    assert len(feedback) == len(word) == len(guess), 'guess, feedback and word must be of the same length'

    if feedback == get_feedback(guess, word):
        return True
    else:
        return False

@lru_cache()
def get_feedback(guess: str, answer: str) -> list[str]:
    """get feedback from guess and answer"""
    assert len(guess) == len(answer), 'guess and answer must be of the same length'
    guess = guess.lower()

    n = len(guess)
    taken = [False]*n # specify which letters are used up for count constraint
    feedback = ['b']*n
    # b - black, g - green, y - yellow

    for i in range(n):

        # handle green
        if guess[i] == answer[i]:
            feedback[i] = 'g'
            taken[i] = True
            continue
    
        # handle yellow
        for j in range(n): # loop answer
            if guess[i] == answer[j] and not taken[j]:
                feedback[i] = 'y'
                taken[j] = True
    
    return feedback

class Wordle:
    def __init__(
            self, 
            answer: None | str = None,
            max_turn: int = 6, 
        ):
        
        self.max_turn = max_turn
        self.turn = 0
        self.feedbacks = []
        self.guesses = []
        self.status = 'playing'
        self.word_length = 5 # no support for other lengths for now
        assert answer is None or len(answer) == 5, 'answer must be of length 5'

        # initialize answer
        if answer is None:
            self.answer = random.choice(VALID_ANSWERS)
        else:
            self.answer = answer.lower()

    def add_guess(self, guess: str):
        assert self.turn <= self.max_turn, 'maximum turn reached'
        assert len(guess) == self.word_length, 'guess must be of length 5'
        assert guess in VALID_ANSWERS, 'invalid guess'

        feedback = get_feedback(guess, self.answer)

        # update status
        if guess == self.answer:
            self.status = 'win'
        elif len(self.guesses) >= self.max_turn:
            self.status = 'lose'
        self.feedbacks.append(feedback)
        self.guesses.append(guess)
        self.turn += 1

        return self.status, feedback
    
    def get_score(self):
        if self.status == 'lose':
            return -10
        if self.status == 'win':
            return self.turn
        return 0

if __name__ == "__main__":
    wordle = Wordle()

    status, feedback = 'playing', None
    while status == 'playing':
        guess = input('guess : ')
        status, feedback = wordle.add_guess(guess)
        print(f'{status = }')
        print(' '.join(feedback))
        print()
    