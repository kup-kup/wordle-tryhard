import random

with open('valid_words.txt') as f:
    VALID_WORDS = f.read().splitlines()

with open('valid_answers.txt') as f:
    VALID_ANSWERS = f.read().splitlines()

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
    