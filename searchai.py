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

UP, DOWN, LEFT, RIGHT = 0, 1, 2, 3

def count_zeros(board):
    return 16 - np.count_nonzero(board)
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
    move_args = [UP, DOWN, LEFT, RIGHT]
    param = [(move_args[0], board), (move_args[1], board), (move_args[2], board), (move_args[3], board)]

    pool = multiprocessing.Pool(multiprocessing.cpu_count())
    result = pool.map(score_toplevel_move, param)
    
    bestmove = result.index(max(result))

    for m in move_args:
        print("move: %d score: %.4f" % (m, result[m]))

    return bestmove

def score_toplevel_move(args):
    move = args[0]
    board = args[1]

    zeros = count_zeros(board)
    
    depth = 1
    if(zeros < 9):
        depth = 2
    if (zeros < 3):
        depth = 3
    elif (zeros < 1):
        depth = 4

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
    score = 0
    new_board = execute_move(move, board)
    if not board_equals(board, new_board):
        score += score_spawn_possibilities(new_board, depth, prob)
    return score

def score_board(board):
    first_row = 1
    #if(np.count_nonzero(board[0] == 4)):
        #first_row = 5
        #first_row *= board[0][0]/board[0][1]
        #first_row *= board[0][1]/board[0][2]
        #first_row *= board[0][2]/board[0][3]
        #first_row *= np.log2(np.sum(board[0]))
    return count_zeros(board)*smoothness(board) #* (board[0][0]+1) * first_row

def smoothness(board):
    log_board = np.copy(board)
    val = 0
    for i in range(3):
        val += np.sum(abs(log_board[i] - log_board[i+1]))
        val += np.sum(abs(log_board[:,i] - log_board[:,i+1]))
    return (1/(val))

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