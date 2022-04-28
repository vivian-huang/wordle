#!/usr/bin/env python
# coding: utf-8

# In[1]:


import random

from numpy import isin
import pygame
from pygame.locals import *
import sys
import enum
import time
import expected_value_model
import matrix_model

pygame.init()


# In[2]:


#https://colorcodes.io/
white = (255,255,255)
yellow = (202,181,87)
green = (106,172,100)
black = (0,0,0)
gray = (121,125,127)
red = (205,0,26)


# In[3]:


font = pygame.font.SysFont("Helvetica neue", 35)
font.set_bold(True)
small_font = pygame.font.SysFont("Helvetica neue", 25)


# In[4]:


manual_statement = small_font.render("Press 'M' for Manual Wordle", True, black)
automatic_statement = small_font.render("Press 'A' for AI Wordle", True, black)

normal_statement = small_font.render("Press 'N' for Normal Mode", True, black)
hard_statement = small_font.render("Press 'H' for Hard Mode", True, black)


win_statement = font.render("Congrats, You Win!", True, green)
lose_statement = font.render("You Lost :(", True, red)
replay_statement = small_font.render("Press RETURN to Play Again!", True, green)


# In[5]:


class GameDifficulty(enum.Enum):
    normal = 0
    hard = 1

class PlayerMode(enum.Enum):
    manual = 0
    automatic = 1


# In[6]:


class Wordle:
    def __init__(self, difficulty, player_mode, wordle_solutions, possible_guesses):
        self.difficulty = difficulty
        self.player_mode = player_mode
        self.try_count = 0
        self.game_count = 0
        self.solution_set = wordle_solutions
        # self.solution = wordle_solutions[random.randint(0, len(wordle_solutions)-1)].upper()
        self.solution = "CACTI"
        self.possible_guesses = possible_guesses
        # self.guessing_model = expected_value_model.ExpectedValueModel(possible_guesses, self.solution.lower())
        self.guessing_model = matrix_model.MatrixModel(possible_guesses, "crane", self.solution.lower())

    def generate_new_solution(self):
        self.solution = self.solution_set[random.randint(0, len(self.solution_set)-1)].upper()
        self.guessing_model.answer = self.solution.lower()
        if isinstance(self.guessing_model, matrix_model.MatrixModel):
            self.guessing_model.first_guess = True
            self.guessing_model.current_guess = "crane"

    def draw_word(self, guess, word_space, spacing, word_color, word_length, turns, window):

        # word_space = ["","","","","",""]
        # spacing = 0
        # word_color = [white, white, white, white, white]
        # word_length = 5

        for i in range(word_length):
            # print("i: "+str(i))

            word_space[i] = font.render(guess[i], True, white) #rendering word onto screen
            #for each turn/guess, will want to draw word lower down by 80, first one is 50 from top
            #sqr is 50x50
            sqr_graphic = pygame.Rect(60 + spacing, 50 + (turns*80), 50, 50)
            pygame.draw.rect(window, word_color[i], sqr_graphic) #if the first letter is green, the square drawn will be green, etc.
            #drawing letters in rectangles
            letter_graphic = (70+spacing, 50 + turns*80)
            window.blit(word_space[i], letter_graphic)
            spacing += 80 #moves next letter/sqr to the right by 80




    def check_guess(self, turns, answer, guess, window):
        self.try_count += 1
        print("Your current ratio is ", self.get_stats())


        word_space = ["","","","","",""]
        spacing = 0
        word_color = [white, white, white, white, white]
        word_length = 5
        game_turns = turns

        for i, letter in enumerate(guess):
            print(i, letter, guess)
            if letter == answer[i]:
                word_color[i] = green
            elif letter in answer:
                word_color[i] = yellow
            else:
                word_color[i] = gray

        list(guess)
        self.draw_word(guess, word_space, spacing, word_color, word_length, game_turns, window)
        # for i in range(word_length):
        #     word_space[i] = font.render(guess[i], True, white) #rendering word onto screen
        #     #for each turn/guess, will want to draw word lower down by 80, first one is 50 from top
        #     #sqr is 50x50
        #     sqr_graphic = pygame.Rect(60 + spacing, 50 + (turns*80), 50, 50)
        #     pygame.draw.rect(window, word_color[i], sqr_graphic) #if the first letter is green, the square drawn will be green, etc.
        #     #drawing letters in rectangles
        #     letter_graphic = (70+spacing, 50 + turns*80)
        #     window.blit(word_space[i], letter_graphic)
        #     spacing += 80 #moves next letter/sqr to the right by 80

        #win condition
        if word_color == [green, green, green, green, green]:
            return True

    def get_stats(self):
        if self.game_count == 0:
            return self.try_count
        return self.try_count / self.game_count


# In[7]:


def run(width, height, main_fps, main_clock, main_window, wordle_game):
    wordle_game.game_count += 1

    SCREEN_WIDTH = width
    SCREEN_HEIGHT = height
    FPS = main_fps
    clock = main_clock
    window = main_window

    window.fill(white)

    manual_guess = ""
    if wordle_game.player_mode == PlayerMode.automatic:
        ai_guess = wordle_game.guessing_model.next_guess().upper()


    print(wordle_game.solution)

    word_length = 5
    num_guesses = 6
    for x in range(word_length):
        for y in range(num_guesses):
            sqr_graphic = pygame.Rect(60 + 80*x, 50 + (80*y), 50, 50)
            pygame.draw.rect(window, gray, sqr_graphic, 2) #mode 2: unfilled rectangles

    if wordle_game.player_mode == PlayerMode.manual:
        pygame.display.set_caption("MANUAL MODE")
    elif wordle_game.player_mode == PlayerMode.automatic:
        pygame.display.set_caption("AI MODE")

    turns = 0
    win = False

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if wordle_game.player_mode == PlayerMode.manual:
            #user has typed in a letter/pressed key
                if event.type == KEYDOWN:
                    #only allowing alphabet options
                    if event.key == pygame.K_a or event.key == pygame.K_b or event.key == pygame.K_c or event.key == pygame.K_d or event.key == pygame.K_e or event.key == pygame.K_f or event.key == pygame.K_g or event.key == pygame.K_h or event.key == pygame.K_i or event.key == pygame.K_j or event.key == pygame.K_k or event.key == pygame.K_l or event.key == pygame.K_m or event.key == pygame.K_n or event.key == pygame.K_o or event.key == pygame.K_p or event.key == pygame.K_q or event.key == pygame.K_r or event.key == pygame.K_s or event.key == pygame.K_t or event.key == pygame.K_u or event.key == pygame.K_v or event.key == pygame.K_w or event.key == pygame.K_x or event.key == pygame.K_y or event.key == pygame.K_z:
                        manual_guess += event.unicode.upper()
    #                 print("adding character")
    #                 print(len(guess))

                    #won game
                    if event.key == K_RETURN and win == True:
                        # wordle_game.check_guess(turns, wordle_game.solution, manual_guess, window)
                        wordle_game.generate_new_solution()

                        run(SCREEN_WIDTH, SCREEN_HEIGHT, FPS, clock, window, wordle_game)

                    #ran out of turns
                    if event.key == K_RETURN and turns > 5:
                        wordle_game.generate_new_solution()
                        run(SCREEN_WIDTH, SCREEN_HEIGHT, FPS, clock, window, wordle_game)

                    #user is typing more than five letters
                    if len(manual_guess) > 5:
                        manual_guess = manual_guess[0:5]

                    #user backspaced
                    if event.key == K_BACKSPACE:
                        #removing last one
                        manual_guess = manual_guess[:-1]
                    print("manual_guess: ")
                    print(manual_guess)
                    print(manual_guess in wordle_game.possible_guesses)
                    if event.key == K_RETURN and len(manual_guess) > 4 and manual_guess.lower() in wordle_game.possible_guesses:
                        win = wordle_game.check_guess(turns, wordle_game.solution, manual_guess, window)
                        turns += 1

                        #restart guess
                        manual_guess = ""
                        #black out bottom of screen where guess was previously
                        window.fill(white, (0, 500, 500, 200))

            elif wordle_game.player_mode == PlayerMode.automatic:
#                 time.sleep(1)
                print("we are in automatic")
                print("turns" + str(turns))
                print(wordle_game.guessing_model.possible_guesses)

                # ai_guess = wordle_game.guessing_model.next_guess().upper()
                print("HERE: ", ai_guess)

                if event.type == KEYDOWN:

                    if event.key == K_RETURN and win == True:
                        wordle_game.generate_new_solution()
                        wordle_game.guessing_model.possible_guesses = wordle_game.possible_guesses
                        run(SCREEN_WIDTH, SCREEN_HEIGHT, FPS, clock, window, wordle_game)

                    #if press return and ran out of turns
                    if event.key == K_RETURN and turns > 5:
                        wordle_game.generate_new_solution()

                        wordle_game.guessing_model.possible_guesses = wordle_game.possible_guesses
                        run(SCREEN_WIDTH, SCREEN_HEIGHT, FPS, clock, window, wordle_game)

                    if event.key == K_RETURN:

    #                 if len(ai_guess) > 4:
                        win = wordle_game.check_guess(turns, wordle_game.solution, ai_guess, window)
                        turns += 1

                        ai_guess = wordle_game.guessing_model.next_guess().upper()

        if wordle_game.player_mode == PlayerMode.manual:
            window.fill(white, (0, 500, 500, 200))
            guess_graphic = font.render(manual_guess, True, black)
            window.blit(guess_graphic, (180, 530))
        elif wordle_game.player_mode == PlayerMode.automatic:
            window.fill(white, (0, 500, 500, 200))
            guess_graphic = font.render(ai_guess, True, black)
            window.blit(guess_graphic, (180, 530))

        #end game text
#         print("turns: " + str(turns))
#         print(win)
        if win == True:
            #black out entire screen
            window.fill(white)

            win_pos = win_statement.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2-50))
            replay_pos = replay_statement.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2+50))

            window.blit(win_statement, win_pos)
            window.blit(replay_statement, replay_pos)
#             window.blit(replay_statement, (60, 300))
        elif turns > 5 and win != True:
#             print("you lost")
            window.fill(white)
            lose_pos = lose_statement.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2-50))
            replay_pos = replay_statement.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2+50))
            window.blit(lose_statement, lose_pos)
            window.blit(replay_statement, replay_pos)
#             window.blit(replay_statement, (60, 300))

        #moved run outside
        pygame.display.update()
        clock.tick(FPS)


# In[8]:


def main():

    SCREEN_WIDTH = 500
    SCREEN_HEIGHT = 600

    FPS=30
    clock = pygame.time.Clock()

    window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    window.fill(white)

    manual_pos = manual_statement.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2-50))
    auto_pos = automatic_statement.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2+50))

    window.blit(manual_statement, manual_pos)
    window.blit(automatic_statement, auto_pos)

    pygame.display.set_caption("WORDLE")

    file1 = open("wordle_solutions.txt","r")
    wordle_solutions = file1.readlines()

    file2 = open("common.txt","r")
    possible_guesses = file2.read().splitlines()
#     print("possible_guesses type:")
#     print(type(possible_guesses))
#     print(possible_guesses)

#     manual_bool = None

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        #user has typed in a letter/pressed key
            if event.type == KEYDOWN:
                #have not yet set automatic or manual mode
#                 if manual_bool is None:
                if event.key == pygame.K_a:
                    print("testing automatic")
                    manual_bool = False
                    window.fill(white)
#                     normal_pos = normal_statement.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2-50))
#                     hard_pos = hard_statement.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2+50))
#                     window.blit(normal_statement, normal_pos)
#                     window.blit(hard_statement, hard_pos)
                    wordle_game = Wordle(GameDifficulty.normal, PlayerMode.automatic, wordle_solutions, possible_guesses)

                    run(SCREEN_WIDTH, SCREEN_HEIGHT, FPS, clock, window, wordle_game)

                if event.key == pygame.K_m:
                    print("testing manual")
                    manual_bool = True
                    window.fill(white)
#                     normal_pos = normal_statement.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2-50))
#                     hard_pos = hard_statement.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2+50))
#                     window.blit(normal_statement, normal_pos)
#                     window.blit(hard_statement, hard_pos)
                    wordle_game = Wordle(GameDifficulty.normal, PlayerMode.manual, wordle_solutions, possible_guesses)
                    run(SCREEN_WIDTH, SCREEN_HEIGHT, FPS, clock, window, wordle_game)

                #have set automatic/manual and now need to set normal/hard
#                 if manual_bool is not None:
#                     if event.key == pygame.K_n and manual_bool == True:
#                         print("in manual normal mode")
#                         wordle_game = Wordle(GameDifficulty.normal, PlayerMode.manual, wordle_solutions, possible_guesses)
#                         run(SCREEN_WIDTH, SCREEN_HEIGHT, FPS, clock, window, wordle_game)
#                     if event.key == pygame.K_n and manual_bool == False:
#                         print("in automatic normal mode")
#                         wordle_game = Wordle(GameDifficulty.normal, PlayerMode.automatic, wordle_solutions, possible_guesses)
#                         run(SCREEN_WIDTH, SCREEN_HEIGHT, FPS, clock, window, wordle_game)
#                     if event.key == pygame.K_h and manual_bool == True:
#                         print("in manual hard mode")
#                         wordle_game = Wordle(GameDifficulty.hard, PlayerMode.manual, wordle_solutions, possible_guesses)
#                         run(SCREEN_WIDTH, SCREEN_HEIGHT, FPS, clock, window, wordle_game)
#                     if event.key == pygame.K_h and manual_bool == False:
#                         print("in automatic hard mode")
#                         wordle_game = Wordle(GameDifficulty.hard, PlayerMode.automatic, wordle_solutions, possible_guesses)
#                         run(SCREEN_WIDTH, SCREEN_HEIGHT, FPS, clock, window, wordle_game)



        pygame.display.update()
        clock.tick(FPS)


# In[9]:


main()
