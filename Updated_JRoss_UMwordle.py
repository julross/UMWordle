from turtle import TurtleScreen
import pygame

pygame.init()

secret_word = input("What is the secret word? ")

#to set up the game screen/display
white = (255, 255, 255)
black = (0, 0, 0)
green = (0, 100, 0)
blue = (0, 0, 255)
orange = (219, 101, 42)
turn = 0
WIDTH = 600
HEIGHT = 700
display = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("UM-wordle")

board = [[" ", " ", " ", " ", " "],
         [" ", " ", " ", " ", " "],
         [" ", " ", " ", " ", " "],
         [" ", " ", " ", " ", " "],
         [" ", " ", " ", " ", " "],
         [" ", " ", " ", " ", " "]]


#create timer and framerate to control speed of game 
fps = 60 #to run at the same speed on all machines
timer = pygame.time.Clock()

title_font = pygame.font.Font('freesansbold.ttf', 56)
text_font = pygame.font.Font('freesansbold.ttf', 17)
game_over = False 
letters = 0
turn_live = True 

def create_board():
    global turn 
    global board 
    for col in range(0, len(secret_word)): #range is start inclusive
        for row in range(0, 6):
            pygame.draw.rect(display, white, [col * 100 + 10, row * 100 + 10, 84, 84], 2) #(x,y) start coord., width, height, hollow rects w border 2)
            letter_text = title_font.render(board[row][col], True, white)
            display.blit(letter_text, (col * 100 + 30, row * 100 + 25))
    pygame.draw.rect(display, blue, pygame.Rect(len(secret_word) * 100, turn * 100 + 10, 90, 30)) #right, down, width, length 
    move_text = text_font.render("Next Move", True, white) 
    display.blit(move_text, (len(secret_word)*100, turn*100 + 19)) #to indicate which row/round user is on
    if game_over == True:
        pygame.draw.rect(display, black, pygame.Rect(len(secret_word) * 100, turn * 100 + 10, 90, 30))

def check_words():
    global turn 
    global board 
    global secret_word
    for col in range(0, len(secret_word)):
        for row in range(0, 6):
            if secret_word[col] == board[row][col] and turn > row:
                pygame.draw.rect(display, green, [col * 100 + 10, row * 100 + 10, 84, 84], 0)
            elif board[row][col] in secret_word and turn > row: 
                pygame.draw.rect(display, orange, [col * 100 + 10, row * 100 + 10, 84, 84], 0)

#main game loop
running = True
while running:
    timer.tick(fps)
    display.fill(black)
    check_words()
    create_board()

    for event in pygame.event.get(): #make sure to exit to avoid infinite loop
        if event.type == pygame.QUIT:
            running = False #out of infinite loop
        if event.type == pygame.TEXTINPUT and turn_live and not game_over:
            item = event.__getattribute__("text") #checks for a key equal to "text" in attribute's dictionary
            board[turn][letters] = item #writing the item user entered to board
            letters += 1
        if event.type == pygame.KEYDOWN: 
            if event.key == pygame.K_BACKSPACE and letters > 0: 
                board[turn][letters - 1] = " "
                letters -= 1
            if event.key == pygame.K_RETURN and not game_over:
                turn += 1
                letters = 0
            if event.key == pygame.K_RETURN and game_over:
                turn = 0
                letters = 0
                game_over = False 
                board = [[" ", " ", " ", " ", " "],
                         [" ", " ", " ", " ", " "],
                         [" ", " ", " ", " ", " "],
                         [" ", " ", " ", " ", " "],
                         [" ", " ", " ", " ", " "],
                         [" ", " ", " ", " ", " "]]
        
    for row in range(0, 6):
        if len(secret_word) == 5:
            guess = board[row][0] + board[row][1] + board[row][2] + board[row][3] + board[row][4]
        elif len(secret_word) == 4:
            guess = board[row][0] + board[row][1] + board[row][2] + board[row][3]
        elif len(secret_word) == 3:
            guess = board[row][0] + board[row][1] + board[row][2]
        elif len(secret_word) == 2:
            guess = board[row][0] + board[row][1]
        elif len(secret_word) == 1:
            guess = board[row][0]
        if guess == secret_word and row < turn: 
            game_over = True 

    if letters == len(secret_word):
        turn_live = False
    if letters < len(secret_word):
        turn_live = True 
    
    if turn == 6:
        game_over = True 
        lost_text = title_font.render("You lost", True, orange)
        display.blit(lost_text, (190, 619))

    if game_over and turn < 6:
        won_text = title_font.render("You won", True, green)
        display.blit(won_text, (190, 619))

    pygame.display.flip()
pygame.quit()



