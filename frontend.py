#!/usr/bin/env python
# coding: utf-8

# In[1]:


import random
import pygame
from pygame.locals import *
import sys
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


win_statement = font.render("Congrats, You Win!", True, green)
lose_statement = font.render("You Lost :(", True, red)
replay_statement = small_font.render("Press RETURN to Play Again!", True, green)


# In[5]:


def checkGuess(turns, answer, guess, window):
    word_space = ["","","","","",""]
    spacing = 0
    word_color = [white, white, white, white, white]
    word_length = 5
    
    for i, letter in enumerate(guess):
        if letter == answer[i]:
            word_color[i] = green
        elif letter in answer:
            word_color[i] = yellow
        else:
            word_color[i] = gray
            
    list(guess)
    
    for i in range(word_length):
        word_space[i] = font.render(guess[i], True, white) #rendering word onto screen
        #for each turn/guess, will want to draw word lower down by 80, first one is 50 from top
        #sqr is 50x50
        sqr_graphic = pygame.Rect(60 + spacing, 50 + (turns*80), 50, 50)
        pygame.draw.rect(window, word_color[i], sqr_graphic) #if the first letter is green, the square drawn will be green, etc.
        #drawing letters in rectangles
        letter_graphic = (70+spacing, 50 + turns*80)
        window.blit(word_space[i], letter_graphic)
        spacing += 80 #moves next letter/sqr to the right by 80
    
    #win condition
    if word_color == [green, green, green, green, green]:
        return True
        


# In[6]:


def main():
    file = open("wordle_solutions.txt","r")
    wordle_solutions = file.readlines()
    actual_word = wordle_solutions[random.randint(0, len(wordle_solutions)-1)].upper()
    
    SCREEN_WIDTH = 500    
    SCREEN_HEIGHT = 600

    FPS=30
    clock = pygame.time.Clock()
    
    window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    window.fill(white)
    
    guess = ""
    
    print(actual_word)
    
    word_length = 5
    num_guesses = 6
    for x in range(word_length):
        for y in range(num_guesses):
            sqr_graphic = pygame.Rect(60 + 80*x, 50 + (80*y), 50, 50)
            pygame.draw.rect(window, gray, sqr_graphic, 2) #mode 2: unfilled rectangles
            
    pygame.display.set_caption("WORDLE")
    
    turns = 0
    win = False
    
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            
            #user has typed in a letter/pressed key
            if event.type == KEYDOWN:
                guess += event.unicode.upper()
                
                #won game
                if event.key == K_RETURN and win == True:
                    main()
                
                #ran out of turns
                if event.key == K_RETURN and turns > 5:
                    main()
                
                #user is typing more than five letters
                if len(guess) > 5:
                    guess = guess[0:5]
                
                #user backspaced
                if event.key == K_BACKSPACE:
                    #removing last one
                    guess = guess[:-1]
                    
                if event.key == K_RETURN and len(guess) > 4:
                    win = checkGuess(turns, actual_word, guess, window)
                    turns += 1
                    
                    #restart guess
                    guess = ""
                    #black out bottom of screen where guess was previously
                    window.fill(white, (0, 500, 500, 200))
                    
        window.fill(white, (0, 500, 500, 200))
        guess_graphic = font.render(guess, True, black)
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
            
        pygame.display.update()
        clock.tick(FPS)
                    


# In[7]:


main()


# In[ ]:


#TODO: fix returning early + backspacing (only works when backspacing last letter)
#TODO: center text for end statements

