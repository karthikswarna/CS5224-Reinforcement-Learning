#import modules
import pygame
from pygame.locals import *
import numpy as np
import random

pygame.init()

screen_height = 300
screen_width = 300
line_width = 6
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Tic Tac Toe')

#define colours
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

#define font
font = pygame.font.SysFont(None, 40)

#define variables
clicked = False
player = 1
pos = (0,0)
markers = []
game_over = False
winner = 0

#setup a rectangle for "Play Again" Option
again_rect = Rect(screen_width // 2 - 80, screen_height // 2, 160, 50)

#create empty 3 x 3 list to represent the grid
for x in range (3):
	row = [0] * 3
	markers.append(row)



def draw_board():
	bg = (255, 255, 210)
	grid = (50, 50, 50)
	screen.fill(bg)
	for x in range(1,3):
		pygame.draw.line(screen, grid, (0, 100 * x), (screen_width,100 * x), line_width)
		pygame.draw.line(screen, grid, (100 * x, 0), (100 * x, screen_height), line_width)

def draw_markers():
	x_pos = 0
	for x in markers:
		y_pos = 0
		for y in x:
			if y == 1:
				pygame.draw.line(screen, red, (x_pos * 100 + 15, y_pos * 100 + 15), (x_pos * 100 + 85, y_pos * 100 + 85), line_width)
				pygame.draw.line(screen, red, (x_pos * 100 + 85, y_pos * 100 + 15), (x_pos * 100 + 15, y_pos * 100 + 85), line_width)
			if y == -1:
				pygame.draw.circle(screen, green, (x_pos * 100 + 50, y_pos * 100 + 50), 38, line_width)
			y_pos += 1
		x_pos += 1	


def check_game_over():
	global game_over
	global winner

	x_pos = 0
	for x in markers:
		#check columns
		if sum(x) == 3:
			winner = 1
			game_over = True
		if sum(x) == -3:
			winner = 2
			game_over = True
		#check rows
		if markers[0][x_pos] + markers [1][x_pos] + markers [2][x_pos] == 3:
			winner = 1
			game_over = True
		if markers[0][x_pos] + markers [1][x_pos] + markers [2][x_pos] == -3:
			winner = 2
			game_over = True
		x_pos += 1

	#check cross
	if markers[0][0] + markers[1][1] + markers [2][2] == 3 or markers[2][0] + markers[1][1] + markers [0][2] == 3:
		winner = 1
		game_over = True
	if markers[0][0] + markers[1][1] + markers [2][2] == -3 or markers[2][0] + markers[1][1] + markers [0][2] == -3:
		winner = 2
		game_over = True

	#check for tie
	if game_over == False:
		tie = True
		for row in markers:
			for i in row:
				if i == 0:
					tie = False
		#if it is a tie, then call game over and set winner to 0 (no one)
		if tie == True:
			game_over = True
			winner = 0

def draw_game_over(winner):
	if winner == 1:
		end_text = "You win!"
	elif winner == 2:
		end_text = "Computer wins!"
	elif winner == 0:
		end_text = "You have tied!"

	end_img = font.render(end_text, True, blue)
	pygame.draw.rect(screen, green, (screen_width // 2 - 100, screen_height // 2 - 60, 200, 50))
	screen.blit(end_img, (screen_width // 2 - 100, screen_height // 2 - 50))

	again_text = 'Play Again?'
	again_img = font.render(again_text, True, blue)
	pygame.draw.rect(screen, green, again_rect)
	screen.blit(again_img, (screen_width // 2 - 80, screen_height // 2 + 10))

    
#*********************************Custom Functions************************************
def create_trans_matrix(trans_matrix):
    state_list = []
    state_list.append("000000000")
    
    for state in state_list:
        trans_matrix[state] = {}
        for index, pos in enumerate(state):
            if(pos == '0'):
                intermediate_state = state[:index] + '1' + state[index + 1:]
                trans_matrix[state][index] = {}

                sum = 0
                for index2, pos2 in enumerate(intermediate_state):
                    if(pos2 == '0'):
                        new_state = intermediate_state[:index2] + '2' + intermediate_state[index2 + 1:]
                        if(new_state not in state_list):
                            state_list.append(new_state)
                        trans_matrix[state][index][new_state] = np.random.random()
                        sum += trans_matrix[state][index][new_state]
                trans_matrix[state][index] = { k:v/sum for (k,v) in trans_matrix[state][index].items()}

def board_to_state(board):
    state = "000000000"
    for x, row in enumerate(board):
        for y, cell in enumerate(row):
            if cell == 1:
                state = state[:y + 3*x] + '1' + state[y + 3*x + 1:]
            elif cell == -1:
                state = state[:y + 3*x] + '2' + state[y + 3*x + 1:]

    return state
                
def state_to_board(state):
    board = []
    for x in range (3):
        row = [0] * 3
        board.append(row)
    
    for index, value in enumerate(state):
        if value == '1':
            board[int(index)//3][int(index)%3] = 1
        elif value == '2':
            board[int(index)//3][int(index)%3] = -1
    
    return board
#************************************************************************************


# Create Probability Transition matrix.
trans_matrix = {}
create_trans_matrix(trans_matrix)

#main loop
run = True
while run:

    #draw board and markers first
    draw_board()
    draw_markers()

    #handle events
    for event in pygame.event.get():
        #handle game exit
        if event.type == pygame.QUIT:
            run = False
        #run new game
        if game_over == False:
            #check for mouseclick
            if event.type == pygame.MOUSEBUTTONDOWN and clicked == False:
                clicked = True
            if event.type == pygame.MOUSEBUTTONUP and clicked == True:
                clicked = False
                pos = pygame.mouse.get_pos()
                cell_x = pos[0] // 100
                cell_y = pos[1] // 100
                if markers[cell_x][cell_y] == 0:
                    initial_state = board_to_state(markers)
                    position = cell_y + 3*cell_x
                    next_possible_states = trans_matrix[initial_state][position]
                    if next_possible_states:	# if next_possible_states are empty. i.e current state is not 4X, 4O state.
                        # next_state = max(next_possible_states, key=next_possible_states.get) # Select most probable state
                        # next_state = random.choice(list(next_possible_states))               # Select a random state.
                        next_state = np.random.choice(list(next_possible_states), p=list(next_possible_states.values()))

                    # Player's move
                    markers[cell_x][cell_y] = player
                    check_game_over()
                    
                    if game_over == False:
                        # Computer's move
                        markers = state_to_board(next_state)
                        check_game_over()


    #check if game has been won
    if game_over == True:
        draw_game_over(winner)
        #check for mouseclick to see if we clicked on Play Again
        if event.type == pygame.MOUSEBUTTONDOWN and clicked == False:
            clicked = True
        if event.type == pygame.MOUSEBUTTONUP and clicked == True:
            clicked = False
            pos = pygame.mouse.get_pos()
            if again_rect.collidepoint(pos):
                #reset variables
                game_over = False
                player = 1
                pos = (0,0)
                markers = []
                winner = 0
                #create empty 3 x 3 list to represent the grid
                for x in range (3):
                    row = [0] * 3
                    markers.append(row)
                
				# These two lines create new transition matrix for every run.
                # trans_matrix = {}
                # create_trans_matrix(trans_matrix)


    #update display
    pygame.display.update()

pygame.quit()