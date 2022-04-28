import random
import time
import collections
class MatrixModel:
    def __init__(self, possible_words, starting_word, final_answer):
        self.current_guess = starting_word
        self.answer = final_answer
        self.gray_letters = []
        self.possible_guesses = possible_words
        self.freq_scoring = {'q': 26, 'j': 25, 'z': 24, 'x': 23, 'v': 22, 'w': 21, 'f': 20, 'k': 19, 'b': 18, 'g': 17, 'm': 16, 'h': 15, 'y': 14, 'p': 13, 'u': 12, 'c': 11, 'n': 10, 'd': 9, 'l': 8, 'i': 7, 't': 6, 'o': 5, 'r': 4, 'a': 3, 's': 2, 'e': 1}

        
    # This function determines if a guess is valid given the feedback that's been given from guesses 
    # till this point yellow letters is a list of all letters of the guess that are correct but in the wrong 
    # position green letters is a tuple list of all leters of the guess that are in the correct position and 
    # spot with the letters respective position in the tuple list, example green_letters = [('h',2), ('e',3)]
    def _valid_guess(self, guess, green_letters, yellow_letters, gray_letters):
        for letter_tuple in yellow_letters:
            if letter_tuple[0] not in guess or guess[letter_tuple[1]] == letter_tuple[0]:
                return False
        for letter_tuple in green_letters:
            if guess[letter_tuple[1]] != letter_tuple[0]:
                return False
        for letter in gray_letters:
            if letter in guess:
                return False
        return True
    
    # This function provides feedback for a guess given some answer, the notation of the feedback is seen below
    # For a given word heart, the notation used throughout the model is as follows
    # Each letter is given a score of 0, 1, or 2. 0 means that the letter does not exist in the correct answer. 
    # 1 means the letter is yellow, correct letter wrong spot. 2 menas the lettter is green, correct letter and correct
    # spot. if the answer is harsh and our guess is heart, then the resulting notation would be:
    # [('h',2),('e',0),('a',1),('r',0), ('t',0)]
    def _score_guess(self, answer, guess):
        guess_feedback = []
        for i in range(5):
            if guess[i] == answer[i]:
                guess_feedback.append((guess[i],2))
            elif guess[i] in answer:
                guess_feedback.append((guess[i],1))
            else:
                guess_feedback.append((guess[i],0))
        return guess_feedback
    # This function creates a frequency scoring 
    def _score_frequency(self, word):
        score = 0
        for letter in word:
            score += self.freq_scoring[letter]
        return score
    # This function takes feedback in the above form and converts it into a list of green, yellow, and 
    # gray letters green letters and yellow letters are stored in tuples of the letter and their index within 
    # the word gray letters are simply a list of all gray letters
    def _get_green_yellow_gray_letters(self, guess_feedback):
        green_letters = []
        yellow_letters = []
        gray_letters = []
        for index, feedback_tuple in enumerate(guess_feedback):
            if feedback_tuple[1] == 2:
                green_letters.append((feedback_tuple[0], index))
            elif feedback_tuple[1] == 1:
                yellow_letters.append((feedback_tuple[0], index))
            else:
                gray_letters.append(feedback_tuple[0])
        return green_letters, yellow_letters, gray_letters
    
    # This is the main wordle prediction algorithm. It takes in the final_answer we are trying to find, 
    # a current working list of possible guesses, a list of gray letters, and the current guess we have just made
    # It then finds the next guess using a greedy min-max approach 
    def next_guess(self):
        
        # Getting feedback on our current guess based on the answer we're working towards 
        guess_feedback = self._score_guess(self.answer, self.current_guess)
        green_letters, yellow_letters, current_gray_letters = self._get_green_yellow_gray_letters(guess_feedback)
        new_gray_letters = self.gray_letters + current_gray_letters
        new_possible_guesses = []
        
        # Based on the feedback of the guess, narrowing down our list of possible guesses we can chose from
        for guess in self.possible_guesses:
            if self._valid_guess(guess, green_letters, yellow_letters, new_gray_letters):
                new_possible_guesses.append(guess)
        self.possible_guesses = new_possible_guesses

        # Creating the guess answer matrix. This matrix is a matrix of all the possible words by all the possible words.
        # The rows represent the possible guesses and the columns represent the possible answers
        # The value at (guess, answer) represents the number of new possible guesses that exist if we guessed 'guess'
        # and the final answer we were working towards was 'answer'.
        guess_answer_matrix = {}
        for guess in self.possible_guesses:
            guess_answer_matrix[guess] = {}
            for answer in self.possible_guesses:
                guess_feedback = self._score_guess(answer,guess)
                curr_green_letters, curr_yellow_letters, curr_gray_letters = self._get_green_yellow_gray_letters(guess_feedback)
                valid_guesses = 0
                new_possible_guesses = self.possible_guesses.copy()
                new_possible_guesses.remove(guess)
                for option in new_possible_guesses:
                    if self._valid_guess(option,curr_green_letters,curr_yellow_letters, curr_gray_letters):
                        valid_guesses += 1
                guess_answer_matrix[guess][answer] = valid_guesses
        
        # Given this matrix of possible guesses for each guess, answer pair, we find the guess that minimizes the 
        # maximum new possible guesses across all possible answers. This is a greedy minmax approach
        max_guess_dict = {}
        for guess in guess_answer_matrix:
            max_possible_guesses = max(guess_answer_matrix[guess].values())
            max_guess_dict.setdefault(max_possible_guesses,[]).append(guess)
            
        if len(max_guess_dict) == 1:
            min_guess_score = 3000
            min_guess = ''
            for key in max_guess_dict:
                for guess in max_guess_dict[key]:
                    guess_score = self._score_frequency(guess)
                    if guess_score < min_guess_score:
                        min_guess_score = guess_score
                        min_guess = guess
            self.current_guess = min_guess
            

        else: 
            self.current_guess = random.choice(max_guess_dict[min(max_guess_dict.keys())])
        
                
        return self.current_guess
