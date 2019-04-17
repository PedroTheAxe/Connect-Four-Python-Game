#############################
#                           #
# CONNECT FOUR USING PYGAME #
#                           #
#############################
# By Pedro Morais
# Followed Tutorial made by:
# freeCodeCamp.org
# Keith Galli

import numpy as np
import pygame
import sys
import math

#RGB (Red, Green, Blue) initializations

BLUE = (0,0,255) 
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)

pygame.init()

#Variable Definitions

ROW_COUNT = 6
COLUMN_COUNT = 7
SQUARESIZE = 100 #Pixels
WIDTH = COLUMN_COUNT * SQUARESIZE
HEIGHT = (ROW_COUNT+1) * SQUARESIZE
SIZE = (WIDTH, HEIGHT)
RADIUS = int(SQUARESIZE/2 - 5)
GAME_OVER = False
TURN = 0
FONT = pygame.font.SysFont("monospace", 50)

##### Drawing and creating the board #####

def draw_board(board): 
	
	for c in range(COLUMN_COUNT):
		for r in range(ROW_COUNT):
			
			pygame.draw.rect(screen, BLUE, \
			(c * SQUARESIZE, r * SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE)) #The + frees top row
			pygame.draw.circle(screen, BLACK, \
			(int(c * SQUARESIZE + SQUARESIZE/2), int(r * SQUARESIZE + SQUARESIZE + SQUARESIZE/2)), RADIUS)

	for c in range(COLUMN_COUNT):
		for r in range(ROW_COUNT):
			if board[r][c] == 1:
				
				pygame.draw.circle(screen, RED, \
				(int(c * SQUARESIZE + SQUARESIZE/2), HEIGHT - int(r * SQUARESIZE + SQUARESIZE/2)), RADIUS)
			
			elif board[r][c] == 2:
				
				pygame.draw.circle(screen, YELLOW, \
				(int(c * SQUARESIZE + SQUARESIZE/2), HEIGHT - int(r * SQUARESIZE + SQUARESIZE/2)), RADIUS)
	
	pygame.display.update()

def create_board():
	
	board = np.zeros((6,7)) #Matrix of 6 rows * 7 columns 
	return board

board = create_board()
screen = pygame.display.set_mode(SIZE)
draw_board(board)


##### Dropping the piece on the correct spot #####

def drop_piece(board, row, col, piece): #Drops the piece in specific location
	
	board[row][col] = piece 

def is_valid_location(board, col): #Check to see if position in 5th row is still 0
	
	return board[5][col] == 0

def get_next_open_row(board, col): #Checks to see which row will the piece fall on
	
	for r in range(ROW_COUNT):
		if board[r][col] == 0:
			return r

def print_board(board): #Flips the board so that the pieces start from the bottom and go up
	print(np.flip(board, 0))

##### Win Condition #####

def winning_move(board, piece):
	
	#Check for horizontal win
	for c in range(COLUMN_COUNT-3):
		for r in range(ROW_COUNT):
			if board[r][c] == piece and \
			   board[r][c+1] == piece and \
			   board[r][c+2] == piece and \
			   board[r][c+3] == piece:
				
				return True
	
	#Check for vertical win
	for c in range(COLUMN_COUNT):
		for r in range(ROW_COUNT-3):
			if board[r][c] == piece and \
			   board[r+1][c] == piece and \
			   board[r+2][c] == piece and \
			   board[r+3][c] == piece:
				
				return True

	#Check for positive slope (/) diagonal win
	for c in range(COLUMN_COUNT-3):
		for r in range(ROW_COUNT-3):
			if board[r][c] == piece and \
			   board[r+1][c+1] == piece and \
			   board[r+2][c+2] == piece and \
			   board[r+3][c+3] == piece:
		
				return True

	#Check for negative slope (\) diagonal win
	for c in range(COLUMN_COUNT-3):
		for r in range(3, ROW_COUNT):
			if board[r][c] == piece and \
			   board[r-1][c+1] == piece and \
			   board[r-2][c+2] == piece and \
			   board[r-3][c+3] == piece:
			
				return True

###### Game Loop #####

while not GAME_OVER:
	
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()

		if event.type == pygame.MOUSEMOTION: #
			
			pygame.draw.rect(screen, BLACK, (0, 0, WIDTH, SQUARESIZE)) #Erase previous motion
			posx = event.pos[0]
			
			if TURN == 0:
				pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE/2)), RADIUS)
			
			else:
				pygame.draw.circle(screen, YELLOW, (posx, int(SQUARESIZE/2)), RADIUS)
		
		pygame.display.update()

		if event.type == pygame.MOUSEBUTTONDOWN: #When we click the mouse button it will drop the piece in the board
			
			#Player 1 Input
			
			pygame.draw.rect(screen, BLACK, (0, 0, WIDTH, SQUARESIZE)) #Remove victory message overlap

			if TURN == 0:
				
				posx = event.pos[0]
				col = int(math.floor(posx/SQUARESIZE)) #Rounds to nearest integer

				if is_valid_location(board, col):
					
					row = get_next_open_row(board, col)
					drop_piece(board, row, col, 1)

					if winning_move(board, 1):
					
						label = FONT.render("Player 1, you win!", 1, RED)
						screen.blit(label, (40,10))
						GAME_OVER = True

			#Player 2 Input

			else:
				
				posx = event.pos[0]
				col = int(math.floor(posx/SQUARESIZE)) 

				if is_valid_location(board, col):
				
					row = get_next_open_row(board, col)
					drop_piece(board, row, col, 2)

					if winning_move(board, 2):
				
						label = FONT.render("Player 2, you win!", 1, YELLOW)
						screen.blit(label, (40,10))
				
						GAME_OVER = True
			
			draw_board(board)
			TURN += 1
			TURN = TURN % 2

			if GAME_OVER:
				pygame.time.wait(3000) #Time before sys.exit after win (in ms)
