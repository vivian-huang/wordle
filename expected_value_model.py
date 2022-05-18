import math
import random
import numpy as np
from heapq import heappop, heappush, heapify, nlargest

class ExpectedValueModel:
    # WordleGame in frontend.py will read the .txt file and pass in the possible_guesses list.
    def __init__(self, possible_guesses, possible_answers, burn_optimization, burn_word, rhyme_optimization):
        self.original_guess_set = possible_guesses
        self.possible_guesses = possible_guesses
        self.total_bank_size = len(self.possible_guesses)
        self.current_guess = ""
        self.possible_answers = possible_answers
        # self.answer = random.choice(self.possible_answers)
        self.answer = "golly"
        self.turn_count = 0
        self.burn_opt = burn_optimization
        self.burn_word = burn_word
        self.rhyme_opt = rhyme_optimization
        self.rhyme_thrown = False


    def get_word_feedback(self, word, target):
        # print(len(target))
        feedback = []
        seen_count = {}
        for i in range(5):
            # print("word:" + word)
            # print("target:" + target)
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

        pattern_count = {}
        for possible_guess in self.possible_guesses:
            pattern_count[self.get_word_feedback(word, possible_guess)] = \
            pattern_count.get(self.get_word_feedback(word, possible_guess), 0) + 1
        score = 0
        for pattern, _ in pattern_count.items():
            prob = pattern_count[pattern]/float(self.total_bank_size)
            score += prob * math.log2(1/prob)

        return score

    def next_guess(self):
        if self.rhyme_opt:
            scwords = []

        best_word = self.possible_guesses[0]
        best_word_score = self.get_word_score(best_word)

        if self.turn_count == 0:
            best_word = "rates"

        elif (self.burn_opt and self.turn_count > 1) or not self.burn_opt:
            for new_word in self.possible_guesses:
                new_score = self.get_word_score(new_word)
                if self.rhyme_opt:
                    scwords.append((new_score, new_word))

                if not self.rhyme_opt and new_score > best_word_score:
                    best_word = new_word
                    best_word_score = new_score

            if self.rhyme_opt:
                best_words = nlargest(5, scwords)
                if self.turn_count >= 2:
                    tail = best_words[0][1][1:]
                    best_word = ""

                    if all(w[1:] == tail for (_, w) in best_words) and not self.rhyme_thrown:
                        for potential in self.original_guess_set:
                            if sum(1 for (_,w) in best_words if w[0] in potential) >= 3:
                                best_word = potential
                                self.rhyme_thrown = True
                                break

                    if best_word == "":
                        best_word = best_words[0][1]
                else:
                    best_word = best_words[0][1]

        if self.burn_opt:
            if self.turn_count == 0:
                best_word = "rates"

            elif self.turn_count == 1:
                best_word = self.burn_word

        # Need to prune possible guesses
        guess_pattern = self.get_word_feedback(best_word, self.answer)
        new_possible_guesses = []
        for guess in self.possible_guesses:
            if guess_pattern == self.get_word_feedback(best_word, guess):
                new_possible_guesses.append(guess)

        self.possible_guesses = new_possible_guesses
        self.turn_count += 1

        return best_word

    def run_random_games(self):
        number_of_games = 1000
        i = 0
        current_guess_list = []
        guess_count = 0
        while i < number_of_games:
            w = model.next_guess()
            guess_count += 1
            current_guess_list.append(w)
            if w == model.answer:
                print(self.answer, current_guess_list)
                i += 1

                # We need to reset the configuration of the model so that it
                # enters the next game freshly
                self.possible_guesses = self.original_guess_set
                self.answer = random.choice(self.possible_answers)
                current_guess_list = []
                self.turn_count = 0
                if self.burn_opt:
                    self.turn_count = 0

        print("Avg. guesses per game: ", guess_count/number_of_games)

    def run_all_possible_games(self):
        model.answer = self.possible_answers[0]
        number_of_games = len(self.possible_answers) - 1
        # number_of_games = 50

        i = 0
        current_guess_list = []
        guess_count_for_current_game = 0
        all_counts = []
        while i < number_of_games:
            w = model.next_guess()
            guess_count_for_current_game += 1

            current_guess_list.append(w)
            if w == model.answer:
                # print(i, self.answer, current_guess_list)
                i += 1
                all_counts.append(guess_count_for_current_game)
                guess_count_for_current_game = 0

                # We need to reset the configuration of the model so that it
                # enters the next game freshly
                self.possible_guesses = self.original_guess_set
                self.answer = self.possible_answers[i]
                current_guess_list = []
                self.turn_count = 0

        filename = '/Users/vivian/Desktop/burner_and_rhyme_opt.txt'

        with open(filename, mode="w") as outfile:
            for s in all_counts:
                outfile.write("%s\n" % s)

        print("Burn opt:", self.burn_opt, "Using burner word:", self.burn_word, \
            "Rhyme opt:", self.rhyme_opt, ",Avg. guesses per game:", sum(all_counts)/ len(all_counts),\
            "Variance:", np.var(all_counts))



    def find_burner_word(self):
        #Finding burner words to use

        # Find first word without any mutual characters as "rates"
        words_to_score = {}
        for new_word in self.possible_guesses:
            words_to_score[new_word] = self.get_word_score(new_word)
        print("DADADAADA")
        scores = sorted(words_to_score, key=words_to_score.get, reverse=True)

        # Define a "similarity score" as a metric by which the difference between words can
        # be gauged. Higher similarity score means words are more similar
        # 1 point for each similar character in the exact same spot
        # 0.5 points for each shared character that is in a different spot
        for target_score in [0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5]:
            for word in scores[1:]:
                sim_score = 0
                feedback = self.get_word_feedback("rates", word)
                for color in feedback:
                    if color == "green":
                        sim_score += 1
                    elif color == "yellow":
                        sim_score += 0.5
                    # Nothing done for gray, adds nothing to sim_score

                if float(sim_score) == float(target_score):
                    print(word, sim_score)
                    break

my_file = open("common.txt", "r")
guesses = my_file.read()
guess_list = guesses.split("\n")
my_file.close()

my_file = open("wordle_solutions.txt", "r")
solutions = my_file.read()
solution_list = solutions.split("\n")
my_file.close()

# model = ExpectedValueModel(guess_list, solution_list, False, "colin", False)
# model.run_all_possible_games()

# model = ExpectedValueModel(guess_list, solution_list, True, "colin", False)
# model.run_all_possible_games()
#
#
# model = ExpectedValueModel(guess_list, solution_list, False, "colin", True)
# model.run_all_possible_games()
#
#
model = ExpectedValueModel(guess_list, solution_list, True, "colin", True)
model.run_all_possible_games()


# model = ExpectedValueModel(guess_list, solution_list, True, "solid", False)
# model.run_all_possible_games()

# model = ExpectedValueModel(guess_list, solution_list, True, "slide", False)
# model.run_all_possible_games()

# model = ExpectedValueModel(guess_list, solution_list, True, "soled", False)
# model.run_all_possible_games()

# model = ExpectedValueModel(guess_list, solution_list, True, "slate", False)
# model.run_all_possible_games()

# model = ExpectedValueModel(guess_list, solution_list, True, "stare", False)
# model.run_all_possible_games()

# model = ExpectedValueModel(guess_list, solution_list, True, "tires", False)
# model.run_all_possible_games()

# model = ExpectedValueModel(guess_list, solution_list, True, "tales", False)
# model.run_all_possible_games()

# model = ExpectedValueModel(guess_list, solution_list, True, "dates", False)
# model.run_all_possible_games()


# colin 0
# solid 0.5
# slide 1.0
# soled 1.5
# slate 2.0
# stare 2.5
# tires 3.0
# tales 3.5
# dates 4
