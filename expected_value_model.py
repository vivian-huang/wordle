import math
import random

class ExpectedValueModel:
    # WordleGame in frontend.py will read the .txt file and pass in the possible_guesses list.
    def __init__(self, possible_guesses, answer):
        self.original_guess_set = possible_guesses
        self.possible_guesses = possible_guesses
        self.total_bank_size = len(self.possible_guesses)
        self.current_guess = ""
        self.answer = answer


    def get_word_feedback(self, word, target):
        feedback = []
        seen_count = {}
        for i in range(5):
            if word[i] == target[i]:
                feedback.append("green")
                seen_count[word[i]] = seen_count.get(word[i], 0) + 1
            elif word[i] in target and seen_count.get(word[i], 0) < target.count(word[i]):
                feedback.append("yellow")
                seen_count[word[i]] = seen_count.get(word[i], 0) + 1
            else:
                feedback.append("gray")
        return tuple(feedback)

    
    def get_word_score(self, word):
        """
        feedback = {greens: {(1, 's'),(2, 'l')},
                    grays: {'a'}
        }}
        """
        # score = 0
        # # self.patterns = [["gray", "yellow", "gray", "gray", "gray"]]
        # # self.possible_guesses = ["bhels"]
        # for pattern in self.patterns:
        #     valid = 0
        #     for possible_guess in self.possible_guesses:
        #         # print(self.get_word_feedback(word, possible_guess), pattern)
        #         if self.get_word_feedback(word, possible_guess) == pattern:
        #             # print("here")
        #             valid += 1
        #     # print(valid)
        #     prob = float(valid)/float(self.total_bank_size)
        #     # print(valid, prob, self.total_bank_size)
        #     # print(prob)
        #     if prob:
        #         score += prob * math.log(1/prob, 2)

        pattern_count = {}
        for possible_guess in self.possible_guesses:
            pattern_count[self.get_word_feedback(word, possible_guess)] = pattern_count.get(self.get_word_feedback(word, possible_guess), 0) + 1
        score = 0
        for pattern, _ in pattern_count.items():
            prob = pattern_count[pattern]/float(self.total_bank_size)
            score += prob * math.log2(1/prob)

        return score

    def next_guess(self):
        best_word = self.possible_guesses[0]
        best_word_score = self.get_word_score(best_word)
        i = 0
        for new_word in self.possible_guesses:
            # print(i)
            i += 1
            new_score = self.get_word_score(new_word)
            if new_score > best_word_score:
                best_word = new_word
                best_word_score = new_score
        
        # Need to prune possible guesses
        guess_pattern = self.get_word_feedback(best_word, self.answer)
        new_possible_guesses = []
        for guess in self.possible_guesses:
            if guess_pattern == self.get_word_feedback(best_word, guess):
                new_possible_guesses.append(guess)

        self.possible_guesses = new_possible_guesses
        return best_word
    
    def run_games(self):
        number_of_games = 100
        i = 0
        guess_list = []
        guess_count = 0
        while i < number_of_games:
            print("Answer: ", self.answer)
            w = model.next_guess()
            guess_count += 1
            print("Guessed: ", w)
            guess_list.append(w)
            if w == model.answer:
                print(self.answer, guess_list)
                i += 1
                self.possible_guesses = self.original_guess_set
                self.answer = random.choice(self.original_guess_set)
                guess_list = []
        print("Avg. guesses per game: ", guess_count/number_of_games)


        
# model = ExpectedValueModel("", "abcde")
# print(model.get_word_feedback("aaaaa"))

# model = ExpectedValueModel("", "shawl")
# print(model.get_word_feedback("slate"))

# model = ExpectedValueModel("", "abbab")
# print(model.get_word_feedback("bbbbc"))

# my_file = open("common.txt", "r")
# content = my_file.read()
# content_list = content.split("\n")
# my_file.close()

# model = ExpectedValueModel(content_list, random.choice(content_list))

# # model.run_games()