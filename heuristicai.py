import random
import game
import sys
import numpy as np

# Author:				chrn (original by nneonneo)
# Date:				    11.11.2016
# Description:			The logic of the AI to beat the game.

UP, DOWN, LEFT, RIGHT = 0, 1, 2, 3

def find_best_move(board):
    bestmove = -1    

	# TODO:
	# Build a heuristic agent on your own that is much better than the random agent.
	# Your own agent don't have to beat the game.
    print(board)
    
    bestmove = find_best_move_agent(board)
    return bestmove

def find_best_move_random_agent():
    return random.choice([UP,DOWN,LEFT,RIGHT])

def find_best_move_agent(board):
    next_move = UP

    board_up = board.copy()
    board_up = execute_move(UP, board_up)
    print(board_up)
    up_zeros = np.count_nonzero(board_up==0)
    current_zeros = up_zeros
    if (board_equals(board_up, board)):
        current_zeros = -1

    board_down = board.copy()
    board_down = execute_move(DOWN, board_down)
    down_zeros = np.count_nonzero(board_down==0)
    if (down_zeros >= current_zeros and not board_equals(board_down, board)):
        next_move = DOWN
        current_zeros = down_zeros

    board_left = board.copy()
    board_left = execute_move(LEFT, board_left)
    left_zeros = np.count_nonzero(board_left==0)
    if (left_zeros >= current_zeros and not board_equals(board_left, board)):
        next_move = LEFT
        current_zeros = left_zeros

    board_right = board.copy()
    board_right = execute_move(RIGHT, board_right)
    right_zeros = np.count_nonzero(board_right==0)
    if (right_zeros >= current_zeros and not board_equals(board_right, board)):
        next_move = RIGHT
        current_zeros = right_zeros

    return next_move

def execute_move(move, board):
    """
    move and return the grid without a new random tile 
	It won't affect the state of the game in the browser.
    """

    if move == UP:
        return game.merge_up(board)
    elif move == DOWN:
        return game.merge_down(board)
    elif move == LEFT:
        return game.merge_left(board)
    elif move == RIGHT:
        return game.merge_right(board)
    else:
        sys.exit("No valid move")
		
def board_equals(board, newboard):
    """
    Check if two boards are equal
    """
    return  (newboard == board).all()  