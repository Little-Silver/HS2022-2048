import random
import game
import sys
import numpy as np
import multiprocessing
from itertools import product

# Author:      chrn (original by nneonneo)
# Date:        11.11.2016
# Copyright:   Algorithm from https://github.com/nneonneo/2048-ai
# Description: The logic to beat the game. Based on expectimax algorithm.
BOARD_SIZE = 16
BOARD_WIDTH = 4
BOARD_HEIGHT = 4

SCORE_TOP_LEFT = np.array([[2**15, 2**14, 2**13, 2**12], [2**8, 2**9, 2**10, 2**11], [2**7, 2**6, 2**5, 2**4], [0, 2**1, 2**2, 2**3]]) ** 2
# SCORE_TOP_RIGHT = np.array([[2**12, 2**13, 2**14, 2**15], [2**11, 2**10, 2**9, 2**8], [2**4, 2**5, 2**6, 2**7], [2**3, 2**2, 2**1, 0]]) ** 2
# SCORE_BOTTOM_LEFT = np.array([[0, 2**1, 2**2, 2**3], [2**7, 2**6, 2**5, 2**4], [2**8, 2**9, 2**10, 2**11], [2**15, 2**14, 2**13, 2**12]]) ** 2
# SCORE_BOTTOM_RIGHT = np.array([[2**3, 2**2, 2**1, 0], [2**4, 2**5, 2**6, 2**7], [2**11, 2**10, 2**9, 2**8], [2**12, 2**13, 2**14, 2**15]]) ** 2

# SCORE_BOARD_ARR = np.array([SCORE_TOP_LEFT, SCORE_TOP_RIGHT, SCORE_BOTTOM_LEFT, SCORE_BOTTOM_RIGHT])

UP, DOWN, LEFT, RIGHT = 0, 1, 2, 3

def count_zeros(board):
    return (16 - np.count_nonzero(board)) ** 2
# Returns a list of (board, probability) pairs

def score_spawn_possibilities(board, depth, prob):
    prob_2 = 0.9
    prob_4 = 0.1
    score = 1
    for x in range(BOARD_WIDTH):
        for y in range(BOARD_HEIGHT):
            if board[x][y] == 0:
                board_with_2 = np.copy(board)
                board_with_2[x][y] = 2
                score += simulate_move(board_with_2, depth, prob*prob_2)
                board_with_4 = np.copy(board)
                board_with_4[x][y] = 4
                score += simulate_move(board_with_4, depth, prob*prob_4)
    return score

def find_best_move(board):
    """
    find the best move for the next turn.
    """

    bestmove = -1
    UP, DOWN, LEFT, RIGHT = 0, 1, 2, 3
    move_args = [UP,DOWN,LEFT,RIGHT]
    
    result = [score_toplevel_move(i, board) for i in range(len(move_args))]
    bestmove = result.index(max(result))

    for m in move_args:
        print("move: %d score: %.4f" % (m, result[m]))
    return bestmove

def score_toplevel_move(move, board):

    zeros = count_zeros(board)
    
    depth = 1
    if(zeros < 5):
        depth = 2
    if (zeros < 2):
        depth = 3

    return step(board, move, depth, 1)

def simulate_move(board, depth, probability=1):

    if depth == 0:
        return probability * score_board(board)
    
    depth -= 1
    
    score_up = step(board, UP, depth, probability)
    score_left = step(board, LEFT, depth, probability)
    score_down = 0
    #score_right = 0
    #if(score_left == 0 and score_up == 0):
    score_right = step(board, RIGHT, depth, probability)
    #if(score_right == 0):
    score_down = step(board, DOWN, depth, probability)

    return max(score_up, score_down, score_left, score_right)

def step(board, move, depth, prob):
    new_board = execute_move(move, board)
    if board_equals(board, new_board):
        return 0
    else:
        return score_spawn_possibilities(new_board, depth, prob)

def score_board(board):
    board = board.astype(int)

    zeros = count_zeros(board)
    smooth = smoothness(board)
    weight = weighted_board_score(board)

    return weight#int(zeros) * weight*smooth

def smoothness(board):
    log_board = np.copy(board)
    val = 0
    for i in range(3):
        val += np.sum(abs(log_board[i] - log_board[i+1]))
        val += np.sum(abs(log_board[:,i] - log_board[:,i+1]))
    return (1/(val))

def weighted_board_score(board):
    s = 0
    for row in range(BOARD_WIDTH):
        for col in range(BOARD_HEIGHT):
            s += board[row, col] * SCORE_TOP_LEFT[row, col]

    return s

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