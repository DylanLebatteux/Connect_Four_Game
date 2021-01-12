# Imports
import sys
import math
import numpy
import pygame

# Constants
ROW_COUNT = 6
COLUMN_COUNT = 7
SQUARE_SIZE = 100
WIDTH = COLUMN_COUNT * SQUARE_SIZE
HEIGHT = (ROW_COUNT + 1) * SQUARE_SIZE
SIZE = (WIDTH, HEIGHT)
RADIUS = int(SQUARE_SIZE / 2 - 5)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# Function to generate empty board
def create_board():
	board = numpy.zeros((ROW_COUNT, COLUMN_COUNT))
	return board

# Function to add piece in the board
def drop_piece(board, row, col, piece):
	board[row][col] = piece

# Function to check is the location is available
def is_valid_location(board, col):
	return board[5][col] == 0

# Function get the next available row
def get_next_open_row(board, col):
	for r in range(ROW_COUNT):
		if board[r][col] == 0:
			return r

# Function to print the board in right orientation 
def print_board(board):
	print("\n", numpy.flip(board, 0))

# Function to check if their is a winning move
def winning_move(board, piece):
	# Check horizontal locations for win
	for c in range(COLUMN_COUNT - 3):
		for r in range(ROW_COUNT):
			if board[r][c] == piece and board[r][c + 1] == piece and board[r][c + 2] == piece and board[r][c + 3] == piece: 
				return True

	# Check vertical locations for win
	for c in range(COLUMN_COUNT):
		for r in range(ROW_COUNT - 3):
			if board[r][c] == piece and board[r + 1][c] == piece and board[r + 2][c] == piece and board[r + 3 ][c] == piece: 
				return True	

	# Check positively sloped diagonal locations for win
	for c in range(COLUMN_COUNT - 3):
		for r in range(ROW_COUNT - 3):
			if board[r][c] == piece and board[r + 1][c + 1] == piece and board[r + 2][c + 2] == piece and board[r + 3][c + 3] == piece: 
				return True

	# Check negatively sloped diagonal locations for win
	for c in range(COLUMN_COUNT - 3):
		for r in range(3, ROW_COUNT):
			if board[r][c] == piece and board[r - 1][c - 1] == piece and board[r - 2][c - 2] == piece and board[r - 3][c - 3] == piece: 
				return True

# Function to draw the graphical board
def draw_board(board):
	for c in range(COLUMN_COUNT):
		# Draw blue rectangle and black circles for empty postions
		for r in range(ROW_COUNT):
			pygame.draw.rect(screen, BLUE, (c * SQUARE_SIZE, r * SQUARE_SIZE + SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
			pygame.draw.circle(screen, BLACK, (int(c * SQUARE_SIZE + SQUARE_SIZE / 2), int(r * SQUARE_SIZE + SQUARE_SIZE + SQUARE_SIZE / 2)), RADIUS)

	# Draw red and yellow circles for players' pieces
	for c in range(COLUMN_COUNT):
		for r in range(ROW_COUNT):
			if board[r][c] == 1: 
				pygame.draw.circle(screen, RED, (int(c * SQUARE_SIZE + SQUARE_SIZE / 2), HEIGHT - int(r * SQUARE_SIZE + SQUARE_SIZE / 2)), RADIUS)
			elif board[r][c] == 2: 
				pygame.draw.circle(screen, YELLOW, (int(c * SQUARE_SIZE + SQUARE_SIZE / 2), HEIGHT - int(r * SQUARE_SIZE + SQUARE_SIZE / 2)), RADIUS)
	pygame.display.update()

# Variables
board = create_board()
game_over = False
turn = 0
screen = pygame.display.set_mode(SIZE)
draw_board(board)
print_board(board)
pygame.font.init()
font = pygame.font.SysFont("monospace", 70)

# Main loop
while not game_over:
	# Check pygame event
	for event in pygame.event.get():
		# Quit event
		if event.type == pygame.QUIT:
			sys.exit()

		# Mouse motion (postion)
		if event.type == pygame.MOUSEMOTION:
			pos_x = event.pos[0]
			pygame.draw.rect(screen, BLACK, (0, 0, WIDTH, SQUARE_SIZE))
			# Player 1 case
			if turn == 0: 
				pygame.draw.circle(screen, RED, (pos_x, int(SQUARE_SIZE / 2)), RADIUS)
				pygame.display.update()
			# Player 2 case
			else: 
				pygame.draw.circle(screen, YELLOW, (pos_x, int(SQUARE_SIZE / 2)), RADIUS)
				pygame.display.update()

		# Mouse click
		if event.type == pygame.MOUSEBUTTONDOWN:	
			# Player 1 input
			if turn == 0:
				pos_x = event.pos[0]
				col = int(math.floor(pos_x / SQUARE_SIZE))
				if is_valid_location(board, col):
					row = get_next_open_row(board, col)
					drop_piece(board, row, col, 1)
					if winning_move(board, 1):
						pygame.draw.rect(screen, BLACK, (0, 0, WIDTH, SQUARE_SIZE))
						label = font.render("PLAYER 1 WINS !", 1, RED)
						screen.blit(label, (40, 10))
						print("\nPLAYER 1 WINS !")
						game_over = True
			# Player 2 input		
			else:
				pos_x = event.pos[0]
				col = int(math.floor(pos_x / SQUARE_SIZE))
				if is_valid_location(board, col):
					row = get_next_open_row(board, col)
					drop_piece(board, row, col, 2)
					if winning_move(board, 2):
						pygame.draw.rect(screen, BLACK, (0, 0, WIDTH, SQUARE_SIZE))
						label = font.render("PLAYER 2 WINS !", 1, YELLOW)
						screen.blit(label, (40, 10))
						print("\nPLAYER 2 WINS !")
						game_over = True

			# End of the turn
			draw_board(board)
			print_board(board)
			turn += 1
			turn = turn % 2
			if game_over: pygame.time.wait(5000)
	