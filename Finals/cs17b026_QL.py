#import modules
import pygame
from pygame.locals import *
from collections import OrderedDict
from random import randrange
import numpy as np
import operator
import random
import json

#  In state: 1 - X, 2 - O, 0 - Empty
#  In Board: 1 - X, -1 - O, 0 - Empty
#  Winner = Player(1), Computer(2), Tie(0)

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
		end_text = "Player wins!"
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
def create_policy(trans_matrix):
    policy = {}
    for state in trans_matrix:
        selected_index = randrange(state.count('0')) # A random number between 0 and number of empty states in board.
        c = 0
        for index, pos in enumerate(state):
            if pos == '0':
                if c == selected_index:
                    policy[state] = str(index)           # Select selected_index'th empty position in board(i.e '0') as action.
                    break
                c = c + 1

    with open('policy.json', 'w') as f:
        json.dump(policy, f, indent=4)

def policy_evaluation(policy, state_map, trans_matrix, GAMMA, EPSILON):
    converged = False
    V = state_map.copy()
    V = dict.fromkeys(V, 0)     # Value function initialized to zero values.
    newV = V.copy()

    while not converged:
        for state in state_map:
            action = policy[state]

            # Calculating Expected reward given the 'state' and 'action'.
            expectedReward = 0
            for nextState, prob in trans_matrix[state][action].items():
                expectedReward += prob * (reward(state_map, nextState) + GAMMA * V[nextState])
        
            newV[state] = expectedReward

        # Checking for convergence
        converged = True
        for state, value in V.items():
            if abs(value - newV[state]) >= EPSILON:
                converged = False
                break

        # Updating the Value function for next iteration.
        V = newV.copy()
    
    return V

def policy_iteration(state_map, trans_matrix, GAMMA, EPSILON):    
    # Initializing the policy randomly.
    policy = state_map.copy()
    for state in state_map:
        policy[state] = random.choice(list(trans_matrix[state].keys()))    # Randomly initialize using the valid actions.

    stable = False
    i = 0
    while not stable:
        # Evaluating the policy to get value function.
        V = policy_evaluation(policy, state_map, trans_matrix, GAMMA, EPSILON)

        # Policy improvement step using the value function.
        for state in state_map:
            maxValue = float('-inf')
            oldAction = policy[state]

            # Finding the best action using the current value function.
            for action, transitions in trans_matrix[state].items():
                expectedReward = 0
                for nextState, prob in transitions.items():
                    expectedReward += prob * (reward(state_map, nextState) + GAMMA * V[nextState])
                
                if expectedReward > maxValue:
                    maxValue = expectedReward
                    policy[state] = action

            # Check for convergence. i.e If the policy didn't change in an iteration, it converged.
            stable = True
            if oldAction == policy[state]:
                stable = stable and True
            else:
                stable = stable and False
    
    policy = {k:int(v) for k,v in policy.items()}
    with open('policy_policy_iter.json', 'w') as f:
        json.dump(policy, f, indent=4)

def Qlearning(state_map, trans_matrix, STEP, GAMMA, MAX_ITER):
    # Creating and initializing the Q function.
    with open('trans_matrix.json') as f:
        Qe = json.load(f)
    for state, transitions in Qe.items():
        for action in transitions:
            Qe[state][action] = 0

    i = 1
    current_state = "000000000"
    while True:
        possible_actions = list(trans_matrix[current_state].keys())
        action = np.random.choice(possible_actions, p=[1/len(possible_actions)] * len(possible_actions))

        next_possible_states = trans_matrix[current_state][str(action)]
        next_state = np.random.choice(list(next_possible_states), p=list(next_possible_states.values()))

        rew = reward(state_map, next_state)

        maxQ = int(max(Qe[next_state].values()))
        Qe[current_state][action] = Qe[current_state][action] + STEP * (rew + GAMMA * maxQ - Qe[current_state][action])

        if(i % 100000 == 0):
            print("Iteration ", i, ": ")
            print(current_state, " -> ", action, " ", rew, " -> ", next_state)

        if(i > MAX_ITER):
            break
            
        current_state = next_state
        i = i + 1

    # Find optimal policy using the Q values.
    policy = state_map.copy()
    for state in Qe:
        policy[state] = max(Qe[state].items(), key=operator.itemgetter(1))[0]    

    # Store Q and policy functions for reference.
    with open('Q.json', 'w') as f:
        json.dump(Qe, f, indent=4)
    with open('policy.json', 'w') as f:
        json.dump(policy, f, indent=4)

# trans_matrix stores only non-zero probabilities.
def create_trans_matrix():
    trans_matrix = {}
    state_map = OrderedDict()
    state_map["000000000"] = 0
    
    while(len(trans_matrix) != 3139):       # The while loop is included because the 'list(state_map)' iterable doesn't change even after a new element is added to 'state_map' inside the loop.
        for state in list(state_map):       # Iterate over all states and generate.
            if state in trans_matrix:       # If a state is added already, skip it. This is a side-effect for using while loop.
                continue

            # If state is a terminal state.
            if(state_map[state] > 0):
                trans_matrix[state] = {}
                for index in range(9):
                    if state[index] == '0':     # On all valid actions i.e empty places
                        trans_matrix[state][index] = {}
                        trans_matrix[state][index]["000000000"] = 1     # The only possibility is to start a new game.

            # For normal states i.e state_type = 0
            else:
                trans_matrix[state] = {}
                for index, pos in enumerate(state):
                    if(pos == '0'):
                        intermediate_state = state[:index] + '1' + state[index + 1:]    # Making 'X' move.
                        trans_matrix[state][index] = {}

                        sum = 0
                        for index2, pos2 in enumerate(intermediate_state):
                            if(pos2 == '0'):
                                new_state = intermediate_state[:index2] + '2' + intermediate_state[index2 + 1:] # Making 'O' move.
                                new_state_type = get_state_type(new_state)
                                if(new_state not in state_map):         # Add a new_state to the state_map if it is not included previously.
                                    state_map[new_state] = new_state_type
                                    
                                trans_matrix[state][index][new_state] = np.random.random()
                                sum += trans_matrix[state][index][new_state]
                        trans_matrix[state][index] = { k:v/sum for (k,v) in trans_matrix[state][index].items()}
    
    with open('trans_matrix.json', 'w') as f:
        json.dump(trans_matrix, f, indent=4)
    with open('state_map.json', 'w') as f:
        json.dump(state_map, f, indent=4)

# Returns 0 - normal state, 100 - player wins, -100 - computer wins, 10 - tie
def reward(state_map, new_state):
    if(state_map[new_state] == 1):
        return 100
    elif(state_map[new_state] == 2):
        return -100
    elif(state_map[new_state] == 3):
        return 10
    else:
        return 0

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

# Returns 0 - normal state, 1 - player wins, 2 - computer wins, 3 - tie
# For 4X 4O state, it puts X in empty place and then returns the state type.
def get_state_type(state):
    board = state_to_board(state)
    lgame_over = False
    lwinner = 0
    x_pos = 0

    for x in board:
        #check columns
        if sum(x) == 3:             # Check for 'X' first, then for 'O'. The order is important because there can be states like 'XXX 000 OOO' which should be won by 'X'.
            lwinner = 1
            lgame_over = True
        if sum(x) == -3:
            lwinner = 2
            lgame_over = True
        #check rows
        if board[0][x_pos] + board [1][x_pos] + board [2][x_pos] == 3:
            lwinner = 1
            lgame_over = True
        if board[0][x_pos] + board [1][x_pos] + board [2][x_pos] == -3:
            lwinner = 2
            lgame_over = True
        x_pos += 1

    #check cross
    if board[0][0] + board[1][1] + board [2][2] == 3 or board[2][0] + board[1][1] + board [0][2] == 3:
        lwinner = 1
        lgame_over = True
    if board[0][0] + board[1][1] + board [2][2] == -3 or board[2][0] + board[1][1] + board [0][2] == -3:
        lwinner = 2
        lgame_over = True

    #check for tie
    if lgame_over == False:
        tie = True
        zeroCount = 0
        for index, i in enumerate(state):
            if i == '0':
                zeroCount += 1

        if zeroCount == 1:        # 4X 4O situation. We place X in empty position and check.
            for index, i in enumerate(state):
                if i == '0':
                    new_state = state[:index] + '1' + state[index + 1:]
                    return get_state_type(new_state)
        elif zeroCount > 1:
            tie = False

        #if it is a tie, then call game over and set lwinner to 0 (no one)
        if tie == True:
            lgame_over = True
            lwinner = 0

    # Return 0 - normal state, 1 - player wins, 2 - computer wins, 3 - tie
    ret_val = 0
    if(lgame_over == True):
        if(lwinner == 1):
            ret_val = 1
        elif(lwinner == 2):
            ret_val = 2
        else:
            ret_val = 3
    return ret_val
#************************************************************************************


# Create and load Probability Transition matrix.
# create_trans_matrix()
with open('trans_matrix.json') as f:
    trans_matrix = json.load(f)
    
with open('state_map.json') as f:
    state_map = json.load(f)

# Learing using Q value updates and finding optimal policy.
# Qlearning(state_map, trans_matrix, 0.1, 0.85, 3000000)
with open('policy.json') as f: 
    policy = json.load(f)

#main loop
run = True
gameCount = 0
winCount = 0
tieCount = 0
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
            initial_state = board_to_state(markers)

            # Get board position of current action.
            cell_x = int(policy[initial_state]) // 3
            cell_y = int(policy[initial_state]) % 3
            position = cell_y + 3*cell_x
            
            next_possible_states = trans_matrix[initial_state][str(position)]
            if next_possible_states:	                                               # if next_possible_states is not empty. i.e current state is not 4X, 4O state.
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

            if winner == 1:
                winCount += 1
            if winner == 0:
                tieCount += 1
            gameCount += 1
            if gameCount == 1000:
                break

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
                # state_map = OrderedDict()
                # create_trans_matrix(trans_matrix, state_map)


    #update display
    pygame.display.update()

pygame.quit()

print("Played: ", gameCount)
print("Won: ", winCount)
print("Tied: ", tieCount)
print("Lost: ", gameCount - winCount - tieCount)