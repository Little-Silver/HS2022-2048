import random
import game
import sys
import numpy as np

# Author:      chrn (original by nneonneo)
# Date:        11.11.2016
# Copyright:   Algorithm from https://github.com/nneonneo/2048-ai
# Description: The logic to beat the game. Based on expectimax algorithm.
BOARD_SIZE = 16

UP, DOWN, LEFT, RIGHT = 0, 1, 2, 3
max_depth = 2
def count_zeros(board):
    return 16 - np.count_nonzero(board)
# Returns a list of (board, probability) pairs
def find_spawn_possibilities(board):
    zero_elements = count_zeros(board)
    prob_2 = 0.9 / zero_elements
    prob_4 = 0.1 / zero_elements
    possible_boards = np.empty([zero_elements*2,4, 4])
    probabilities = np.empty([zero_elements*2])
    i = -1
    for x in range(len(board)):
        for y in range(len(board[0])):
            if board[x][y] == 0:
                i += 1
                board_with_2 = np.copy(board)
                board_with_2[x][y] = 2
                possible_boards[i] = board_with_2
                probabilities[i] = prob_2
                i += 1
                board_with_4 = np.copy(board)
                board_with_4[x][y] = 4
                possible_boards[i] = board_with_4
                probabilities[i] = prob_4
    return possible_boards, probabilities

def find_best_move(board):
    """
    find the best move for the next turn.
    """
    bestmove = -1
    move_args = [UP,DOWN,LEFT,RIGHT]
    
    result = [score_toplevel_move(i, board) for i in range(len(move_args))]
    bestmove = result.index(max(result))

    for m in move_args:
        print("move: %d score: %.4f" % (m, result[m]))

    return bestmove
    
def score_toplevel_move(move, board):
    if (count_zeros(board) < 4):
        max_depth = 3
    #elif (count_zeros(board) < 3):
    #    depth = 4
    return step(board, move, 1)

	# TODO:
	# Implement the Expectimax Algorithm.
	# 1.) Start the recursion until it reach a certain depth
	# 2.) When you don't reach the last depth, get all possible board states and 
	#		calculate their scores dependence of the probability this will occur. (recursively)
	# 3.) When you reach the leaf calculate the board score with your heuristic.

def simulate_move(board, probability=1, depth=0):

    if depth == max_depth:
        return probability * score_board(board)
    
    depth += 1
    
    score_up = step(board, UP, probability, depth)
    score_left = step(board, LEFT, probability, depth)
    score_down = 0
    score_right = 0
    if(score_left == 0 and score_up == 0):
        score_right = step(board, RIGHT, probability, depth)
        if(score_right == 0):
            score_down = step(board, DOWN, probability, depth)

    return max(score_up, score_down, score_left, score_right)

def step(board, move, prob, depth=0):
    score = 0
    new_board = execute_move(move, board)
    if not board_equals(board, new_board):
        score = 1
        board_possibilities, probabilities = find_spawn_possibilities(new_board)
        for b, p in zip(board_possibilities, probabilities):
            score += simulate_move(b, prob*p, depth)
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
    return (1/np.log2(val))

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
