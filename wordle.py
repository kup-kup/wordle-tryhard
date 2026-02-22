import random

with open('valid_words.txt') as f:
    VALID_WORDS = f.read().splitlines()

with open('valid_answers.txt') as f:
    VALID_ANSWERS = f.read().splitlines()

class Wordle:
    def __init__(
            self, 
            answer: None | str = None,
            max_turn: int = 6, 
        ):
        
        self.max_turn = max_turn
        self.feedback = []
        self.guesses = []
        self.status = 'playing'
        self.word_length = 5 # no support for other lengths for now
        assert answer is None or len(answer) == 5

        # initialize answer
        if answer is None:
            self.answer = random.choice(VALID_ANSWERS)
        else:
            self.answer = answer.lower()

    def add_guess(self, guess):
        assert len(self.guesses) < self.max_turn
        assert len(guess) == self.word_length
        guess = guess.lower()

        taken = [False] * self.word_length # specify which letters are used up for count constraint
        new_feedback = ['b'] * self.word_length
        # b - black, g - green, y - yellow

        for i in range(self.word_length):

            # handle green
            if guess[i] == self.answer[i]:
                new_feedback[i] = 'g'
                taken[i] = True
                continue
        
            # handle yellow
            for j in range(self.word_length): # loop answer
                if guess[i] == self.answer[j] and not taken[j]:
                    new_feedback[i] = 'y'
                    taken[j] = True

        # update status
        if guess == self.answer:
            self.status = 'win'
        elif len(self.guesses) >= self.max_turn:
            self.status = 'lose'
        self.feedback.append(new_feedback)
        self.guesses.append(guess)

        return self.status, new_feedback

if __name__ == "__main__":
    wordle = Wordle()

    status, feedback = 'playing', None
    while status == 'playing':
        guess = input('guess : ')
        status, feedback = wordle.add_guess(guess)
        print(f'{status = }')
        print(' '.join(feedback))
        print()
    