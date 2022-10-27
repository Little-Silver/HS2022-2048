import game
import sys
import numpy as np
import multiprocessing
from itertools import product
import heuristic as ha

UP, DOWN, LEFT, RIGHT = 0, 1, 2, 3

def execute_move(move, board):
    """
    move and return the grid without a new random tile 
	It won't affect the state of the game in the browser.
    """

    UP, DOWN, LEFT, RIGHT = 0, 1, 2, 3

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

def simple_move(board, moveno):
    board_left = game.merge_left(np.copy(board))
    board_up = game.merge_up(np.copy(board))
    board_right = game.merge_right(np.copy(board))

    if(not board_equals(board, board_left) and not board_equals(board, board_up)):
        if(moveno%2 == 0):
            return LEFT
        else:
            return UP
    elif(not board_equals(board, board_left)):
        return LEFT
    elif(not board_equals(board, board_up)):
        return UP 
    elif(not board_equals(board, board_right)):
        return RIGHT
    return UP