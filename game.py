import enum
import csv
import random


class GameDifficulty(enum.Enum):
    normal = 0
    hard = 1


class GameState(enum.Enum):
    in_progress = 0
    victory = 1
    defeat = 2


class PlayerMode(enum.Enum):
    manual = 0
    automatic = 1


class Wordle:
    def __init__(self, answer, difficulty, player_mode):
        self.answer = answer
        self.try_count = 0
        self.difficulty = difficulty
        self.game_state = GameState.in_progress
        self.player_mode = player_mode
        self.feedback = []

    def check_guess(self, guess="_____"):
        if len(guess) != 5:
            raise Exception("Guess must be five letters long.")

        self.try_count += 1

        if self.player_mode == PlayerMode.manual:
            guess = str(input("Enter your guess: "))
            while len(guess) != 5:
                guess = str(input("Your guess must be a five letter word. Enter your guess: "))

        # Correct guess
        if self.answer == guess:
            self.game_state = GameState.victory

        # Wrong guess, no more tries
        elif self.try_count == 5:
            self.game_state = GameState.defeat

        # Wrong guess, more tries left
        else:
            result = []
            for index, c in enumerate(guess):
                if self.answer[index] == c:
                    result.append("green")
                elif c in self.answer:
                    result.append("yellow")
                else:
                    result.append("gray")
            print(result)
            self.feedback.append(result)

    def play(self):
        while self.game_state == GameState.in_progress:
            self.check_guess()
            if self.game_state == GameState.victory:
                print("You won in", self.try_count, "turn(s)!")
            elif self.game_state == GameState.defeat:
                print("You lost! The word was", self.answer)
            else:
                print("You have ", 5 - self.try_count, " tries left.")


if __name__ == "__main__":
    with open("data/solution_set.csv", newline="\n") as f:
        reader = csv.reader(f)
        solution_set = next(reader)

    our_game = Wordle(random.choice(solution_set), GameDifficulty.normal, PlayerMode.manual)
    our_game.play()
