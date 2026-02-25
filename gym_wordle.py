import gymnasium as gym
import numpy as np
from gymnasium import spaces
from wordle import Wordle

with open('valid_answers.txt') as f:
    VALID_ANSWERS = f.read().splitlines()


class GymWordle(gym.Env):
    """A minimal Gymnasium wrapper around the `wordle.Wordle` game."""

    metadata = {}

    def __init__(self, max_turn: int = 6, answer: str | None = None, render_mode: str | None = None):
        super().__init__()
        self.max_turn = max_turn
        self.word_length = 5
        self._fixed_answer = answer
        self.render_mode = render_mode or "human"

        # define action space to be the length of VALID_ANSWERS
        self.action_space = spaces.Discrete(len(VALID_ANSWERS))

        # Observations include encoded guesses and feedback history plus the current turn.
        self.observation_space = spaces.Dict(
            {
                "turn": spaces.Discrete(self.max_turn + 1),
                "guesses": spaces.Box(
                    low=0,
                    high=26,
                    shape=(self.max_turn, self.word_length),
                    dtype=np.int8,
                ),
                "feedback": spaces.Box(
                    low=0,
                    high=3,
                    shape=(self.max_turn, self.word_length),
                    dtype=np.int8,
                ),
            }
        )

        self._rng = np.random.default_rng()
        self._game: Wordle | None = None
        self._guesses = np.full((self.max_turn, self.word_length), 26, dtype=np.int8) # 26 indicates no guess
        self._feedback = np.full((self.max_turn, self.word_length), 3, dtype=np.int8) # 3 indicates no feedback
        self._last_guess: str | None = None
        self.reset()

    def reset(self, *, seed: int | None = None, options=None):
        super().reset(seed=seed)
        if seed is not None:
            self._rng = np.random.default_rng(seed)

        answer = self._fixed_answer or self._rng.choice(VALID_ANSWERS)
        self._game = Wordle(answer=answer, max_turn=self.max_turn)
        self._guesses.fill(26)
        self._feedback.fill(3)
        self._last_guess = None

        return self._get_obs(), {}

    def step(self, action: int):
        assert self._game is not None, "Environment not initialized; call reset() first."
        guess = VALID_ANSWERS[int(action)]
        status, feedback_letters = self._game.add_guess(guess)
        idx = self._game.turn - 1  # turns are 1-based after add_guess
        self._guesses[idx] = self._encode_word(guess)
        self._feedback[idx] = self._encode_feedback(feedback_letters)
        self._last_guess = guess

        terminated = status in {"win", "lose"}
        reward = self._game.get_reward()
        truncated = False
        info = {
            "guess": guess,
            "last_feedback": feedback_letters,
            "answer": self._game.answer,
        }

        return self._get_obs(), reward, terminated, truncated, info

    def render(self):
        if self._last_guess is None:
            print("No guesses yet.")
            return
        latest_feedback = self._feedback[self._game.turn - 1] if self._game else None
        print(f"turn={self._game.turn if self._game else 0} guess={self._last_guess} feedback={latest_feedback}")

    def close(self):
        self._game = None

    def _encode_word(self, word: str) -> np.ndarray:
        # a->0, b->1, ... z->25
        return np.fromiter((ord(c) - 97 for c in word.lower()), dtype=np.int8, count=self.word_length)

    def _encode_feedback(self, fb: list[str]) -> np.ndarray:
        # map b=0, y=1, g=2
        mapping = {"b": 0, "y": 1, "g": 2}
        return np.fromiter((mapping[c] for c in fb), dtype=np.int8, count=self.word_length)

    def _get_obs(self) -> dict:
        turn = 0 if self._game is None else self._game.turn
        return {"turn": turn, "guesses": self._guesses.copy(), "feedback": self._feedback.copy()}