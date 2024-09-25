# Code created by Vatsal Jain 
import pygame
import sys
import csv
import math
import random

pygame.init()
pygame.mixer.init()

pygame.mixer.music.load('calm_music.mp3')
pygame.mixer.music.set_volume(0.5)  # Adjust volume (0.0 to 1.0)
pygame.mixer.music.play(-1)  

click_sound = pygame.mixer.Sound('tch.wav') 
win_sound = pygame.mixer.Sound('win.wav')

# Constants
WIDTH, HEIGHT = 600, 600
LINE_WIDTH = 15
BOARD_ROWS = 3
BOARD_COLS = 3
SQUARE_SIZE = WIDTH // BOARD_COLS
CIRCLE_RADIUS = SQUARE_SIZE // 3
CIRCLE_WIDTH = 15
CROSS_WIDTH = 25
SPACE = SQUARE_SIZE // 4
RED = (255, 0, 0)
BG_COLOR = (28, 170, 156)
LINE_COLOR = (23, 145, 135)
CIRCLE_COLOR = (239, 231, 200)
CROSS_COLOR = (66, 66, 66)

BUTTON_COLOR = (0, 100, 255)
BUTTON_HOVER_COLOR = (0, 150, 255)
BUTTON_TEXT_COLOR = (255, 255, 255)
BUTTON_RECT = pygame.Rect(WIDTH // 2 - 50, HEIGHT // 2 + 50, 100, 50)

# Setup the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Tic Tac Toe')
screen.fill(BG_COLOR)

# Board
board = [[None for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]

# Game variables
player = 'X'
game_over = False

player_wins=0
computer_wins=0
draws=0

# Function to draw lines
def draw_lines():
    # Horizontal lines
    for i in range(1, BOARD_ROWS):
        pygame.draw.line(screen, LINE_COLOR, (0, i * SQUARE_SIZE), (WIDTH, i * SQUARE_SIZE), LINE_WIDTH)
    # Vertical lines
    for i in range(1, BOARD_COLS):
        pygame.draw.line(screen, LINE_COLOR, (i * SQUARE_SIZE, 0), (i * SQUARE_SIZE, HEIGHT), LINE_WIDTH)

# Function to draw X and O
def draw_figures():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 'O':
                pygame.draw.circle(screen, CIRCLE_COLOR, (int(col * SQUARE_SIZE + SQUARE_SIZE // 2), int(row * SQUARE_SIZE + SQUARE_SIZE // 2)), CIRCLE_RADIUS, CIRCLE_WIDTH)
            elif board[row][col] == 'X':
                pygame.draw.line(screen, CROSS_COLOR, (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE), (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SPACE), CROSS_WIDTH)
                pygame.draw.line(screen, CROSS_COLOR, (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SPACE), (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE), CROSS_WIDTH)

# Function to draw vertical winning line
def draw_vertical_winning_line(col, player):
    posX = col * SQUARE_SIZE + SQUARE_SIZE // 2
    if player == 'X':
        color = CROSS_COLOR
    elif player == 'O':
        color = CIRCLE_COLOR
    pygame.draw.line(screen, color, (posX, 15), (posX, HEIGHT - 15), LINE_WIDTH)

# Function to draw horizontal winning line
def draw_horizontal_winning_line(row, player):
    posY = row * SQUARE_SIZE + SQUARE_SIZE // 2
    if player == 'X':
        color = CROSS_COLOR
    elif player == 'O':
        color = CIRCLE_COLOR
    pygame.draw.line(screen, color, (15, posY), (WIDTH - 15, posY), LINE_WIDTH)

# Function to draw ascending diagonal line
def draw_asc_diagonal(player):
    if player == 'X':
        color = CROSS_COLOR
    elif player == 'O':
        color = CIRCLE_COLOR
    pygame.draw.line(screen, color, (15, HEIGHT - 15), (WIDTH - 15, 15), LINE_WIDTH)

# Function to draw descending diagonal line
def draw_desc_diagonal(player):
    if player == 'X':
        color = CROSS_COLOR
    elif player == 'O':
        color = CIRCLE_COLOR
    pygame.draw.line(screen, color, (15, 15), (WIDTH - 15, HEIGHT - 15), LINE_WIDTH)

def restart():
    global board, player, game_over
    board = [[None for _ in range(BOARD_COLS)] for _ in range(BOARD_COLS)]
    player = 'X'
    game_over = False
    screen.fill(BG_COLOR)
    draw_lines()
    pygame.display.update()

def check_csv(board_string,player):
    with open('state.csv', mode='r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            if row['board_string'] == board_string and row['player'] == player:
                return row['position']
    return "" 
  
def write_csv(board_string,player, position):
    with open('state.csv', mode='a', newline='') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow([board_string,player, position])
        
def make_csv():
    with open('state.csv', mode='w', newline='') as file:
        fieldnames = ['board_string','player', 'position']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        
# make_csv() DONT RUN THIS LINE

# Minimax algorithm
def minimax(board, is_maximizing):
    if check_win('X'):
        return 1 
    if check_win('O'):
        return -1 
    if is_board_full(board):
        return 0
    if is_maximizing:
        best_score = -math.inf
        for i in range(BOARD_COLS):
            for j in range(BOARD_COLS):
                if board[i][j] is None: 
                    board[i][j] = 'X'
                    score = minimax(board, False)
                    board[i][j] = None 
                    best_score = max(score, best_score)
        return best_score
    else:  
        best_score = math.inf
        for i in range(BOARD_COLS):
            for j in range(BOARD_COLS):
                if board[i][j] is None:  
                    board[i][j] = 'O'
                    score = minimax(board, True)
                    board[i][j] = None 
                    best_score = min(score, best_score)
        return best_score

def best_move(board, player):
    board_string = ''.join(board[i][j] if board[i][j] is not None else '.' for i in range(BOARD_COLS) for j in range(BOARD_COLS))
    csv_position = check_csv(board_string, player)
    
    if csv_position:
        row, col = divmod(int(csv_position), BOARD_COLS)  # Convert 1D position to 2D board indices
        return (row, col)
    
    best_score = -math.inf if player == 'X' else math.inf
    best_move = None

    for i in range(BOARD_COLS):
        for j in range(BOARD_COLS):
            if board[i][j] is None: 
                board[i][j] = player  
                score = minimax(board, player == 'O')
                board[i][j] = None 

                if player == 'X':
                    if score > best_score:
                        best_score = score
                        best_move = (i, j)
                else:
                    if score < best_score:
                        best_score = score
                        best_move = (i, j)

    if best_move:
        position = best_move[0] * BOARD_COLS + best_move[1] 
        write_csv(board_string, player, position)
    
    return best_move

def is_board_full(board):
    for row in board:
        if None in row:
            return False
    return True

# function to check if a player has won
def check_win(player):
    for row in range(BOARD_COLS):
        if board[row][0] == board[row][1] == board[row][2] == player:
            return True
    for col in range(BOARD_COLS):
        if board[0][col] == board[1][col] == board[2][col] == player:
            return True
    diag=True
    for row in range(BOARD_COLS):
        if board[row][row] != player:
            diag=False
            break
    if diag:
        return True
    diag=True
    for row in range(BOARD_COLS):
        if board[row][BOARD_COLS-row-1] != player:
            diag=False
            break
    if diag:
        return True
    return False

# Check for a win
def check_win_draw_line(player):
    # Vertical win check
    for col in range(BOARD_COLS):
        if board[0][col] == board[1][col] == board[2][col] == player:
            draw_vertical_winning_line(col, player)
            if player=='X':
                global player_wins
                player_wins+=1
            else:
                global computer_wins
                computer_wins+=1
            win_sound.play()
            return 1

    # Horizontal win check
    for row in range(BOARD_ROWS):
        if board[row][0] == board[row][1] == board[row][2] == player:
            draw_horizontal_winning_line(row, player)
            if player=='X':              
                player_wins+=1
            else:
                computer_wins+=1
            win_sound.play()
            return 1

    # Ascending diagonal win
    if board[2][0] == board[1][1] == board[0][2] == player:
        draw_asc_diagonal(player)
        if player=='X':
            player_wins+=1
        else:
            computer_wins+=1
        win_sound.play()
        return 1

    # Descending diagonal win
    if board[0][0] == board[1][1] == board[2][2] == player:
        draw_desc_diagonal(player)
        if player=='X':
            player_wins+=1
        else:
            computer_wins+=1
        win_sound.play()
        return 1

    return None

def find_random_move(board):
    while True:
        row = random.randint(0, 2)
        col = random.randint(0, 2)
        if board[row][col] is None:
            return row, col

# Function to simulate the computer's move
def play_computer(player, board):
        best = best_move(board, player)
        if best and difficulty=='hard':
            board[best[0]][best[1]] = player
        elif best and difficulty=='easy':
            if random.randint(0, 1) == 0:
                board[best[0]][best[1]] = player
            else:
                row, col = find_random_move(board)
                board[row][col] = player
        elif best and difficulty=='medium':
            if random.uniform(0, 1) < 0.7:
                board[best[0]][best[1]] = player
            else:
                row, col = find_random_move(board)
                board[row][col] = player
            
def draw_restart_screen(player_wins, computer_wins, draws):
    screen.fill(BG_COLOR)
    font = pygame.font.Font(None, 50)
    text = font.render("Game Over", True, (255, 255, 255))
    screen.blit(text, (WIDTH // 2 - 100, HEIGHT // 2 - 250))
    
    # Display Scores
    score_text1 = font.render(f"Player Wins: {player_wins}",True, (255, 255, 255))
    score_text2= font.render(f"Computer Wins: {computer_wins}",True, (255, 255, 255))
    score_text3= font.render(f"Draws: {draws}",True, (255, 255, 255))
    screen.blit(score_text1, (WIDTH // 2 - 200, HEIGHT // 2 - 200))
    screen.blit(score_text2, (WIDTH // 2 - 200, HEIGHT // 2 -150))
    screen.blit(score_text3, (WIDTH // 2 - 200, HEIGHT // 2 -100))
    
    # Restart Button
    restart_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 50, 200, 50)
    pygame.draw.rect(screen, (0, 0, 255), restart_button)
    restart_text = font.render("Restart", True, (255, 255, 255))
    screen.blit(restart_text, (restart_button.x + 25, restart_button.y + 10))
    
    # Difficulty Buttons
    text = font.render("Wanna Change Difficulty?", True, BUTTON_TEXT_COLOR)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 +25))
    draw_button(easy_button_ingame, "Easy")
    draw_button(medium_button_ingame, "Medium")
    draw_button(hard_button_ingame, "Hard")
    pygame.display.update()

    return restart_button


# Main loop
pygame.display.set_caption('Tic Tac Toe')

# Fonts
font = pygame.font.Font(None, 50)
button_font = pygame.font.Font(None, 40)

# Difficulty buttons
easy_button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 60, 200, 50)
medium_button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 +20, 200, 50)
hard_button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 100, 200, 50)

difficulty = None  # This will store the selected difficulty

def draw_menu():
    screen.fill(BG_COLOR)
    text = font.render("Select Difficulty", True, BUTTON_TEXT_COLOR)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - 150))
    draw_button(easy_button_rect, "Easy")
    draw_button(medium_button_rect, "Medium")
    draw_button(hard_button_rect, "Hard")
    pygame.display.update()

def draw_button(button_rect, text):
    mouse_pos = pygame.mouse.get_pos()
    if button_rect.collidepoint(mouse_pos):
        color = BUTTON_HOVER_COLOR
    else:
        color = BUTTON_COLOR
    pygame.draw.rect(screen, color, button_rect)
    button_text = button_font.render(text, True, BUTTON_TEXT_COLOR)
    screen.blit(button_text, (button_rect.x + button_rect.width // 2 - button_text.get_width() // 2, button_rect.y + 10))

menu_screen = True
while menu_screen:
    draw_menu()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            if easy_button_rect.collidepoint(event.pos):
                click_sound.play()
                difficulty = 'easy'
                menu_screen = False 
            if medium_button_rect.collidepoint(event.pos):
                click_sound.play()
                difficulty = 'medium'
                menu_screen = False
            if hard_button_rect.collidepoint(event.pos):
                click_sound.play()
                difficulty = 'hard'
                menu_screen = False  
        pygame.display.update()

screen.fill(BG_COLOR)
# Difficulty buttons ingame
easy_button_ingame = pygame.Rect(WIDTH // 2 -100, HEIGHT // 2 +80, 200, 50)
medium_button_ingame = pygame.Rect(WIDTH // 2 -100, HEIGHT // 2 +150, 200, 50)
hard_button_ingame = pygame.Rect(WIDTH // 2 -100, HEIGHT // 2 + 220, 200, 50)
    
restart_screen=False
draw_lines()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
        if is_board_full(board):
            draws+=1
            game_over = True
            
        if game_over:
            pygame.time.wait(2000)
            board = [[None for _ in range(BOARD_COLS)] for _ in range(BOARD_COLS)]
            button_rect = draw_restart_screen(player_wins, computer_wins, draws)
            restart_screen=True
            game_over = False
            
        elif restart_screen==True:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    click_sound.play()
                    restart()
                    restart_screen=False
                if easy_button_ingame.collidepoint(event.pos):
                    click_sound.play()
                    difficulty = 'easy'
                    restart()
                    restart_screen=False
                if medium_button_ingame.collidepoint(event.pos):
                    click_sound.play()
                    difficulty = 'medium'
                    restart()
                    restart_screen=False
                if hard_button_ingame.collidepoint(event.pos):
                    click_sound.play()
                    difficulty = 'hard'
                    restart()
                    restart_screen=False  
                pygame.display.update()
                
        elif event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            mouseX = event.pos[0]  # X
            mouseY = event.pos[1]  # Y
            clicked_row = mouseY // SQUARE_SIZE
            clicked_col = mouseX // SQUARE_SIZE

            if board[clicked_row][clicked_col] is None:
                board[clicked_row][clicked_col] = player
                click_sound.play()
                draw_figures()
                pygame.display.update()
                if check_win_draw_line(player):
                    game_over = True
                    draw_figures()
                    pygame.display.update()
                else:
                    player = 'O' if player == 'X' else 'X'
                    pygame.time.wait(1000)
                    play_computer(player,board)
                    click_sound.play()
                    draw_figures()
                    pygame.display.update()
                    if check_win_draw_line(player):
                        draw_figures()
                        pygame.display.update()
                        game_over = True
                    player = 'O' if player == 'X' else 'X'

    draw_figures()
    pygame.display.update()
    
pygame.mixer.music.stop()