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

# Returns a list of (board, probability) pairs
def find_spawn_possibilities(board):
    zero_elements = 16 - np.count_nonzero(board)
    prob_2 = 0.9 / zero_elements
    prob_4 = 0.1 / zero_elements
    possible_boards = []

    for x in range(len(board)):
        for y in range(len(board[0])):
            if board[x][y] == 0:
                board_with_2 = np.copy(board)
                board_with_2[x][y] = 2
                board_with_4 = np.copy(board)
                board_with_4[x][y] = 4
                possible_boards.append([board_with_2, prob_2])
                possible_boards.append([board_with_4, prob_4])
    return possible_boards

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

    return step(board, move)

	# TODO:
	# Implement the Expectimax Algorithm.
	# 1.) Start the recursion until it reach a certain depth
	# 2.) When you don't reach the last depth, get all possible board states and 
	#		calculate their scores dependence of the probability this will occur. (recursively)
	# 3.) When you reach the leaf calculate the board score with your heuristic.

def simulate_move(board, probability=1, depth=0):

    if depth == 2:
        return probability * score_board(board)
    
    depth += 1
    
    score_up = step(board, UP, depth)
    score_down = step(board, DOWN, depth)
    score_left = step(board, LEFT, depth)
    score_right = step(board, RIGHT, depth)
    
    return max(score_up, score_down, score_left, score_right)

def step(board, move, depth=0):
    score = 0
    new_board = execute_move(move, board)
    if not board_equals(board, new_board):
        board_possibilities = find_spawn_possibilities(new_board)
        for board_state in board_possibilities:
            current_board = board_state[0]
            current_probability = board_state[1]
            score += simulate_move(current_board, current_probability, depth)
    return score

def score_board(board):
    return np.count_nonzero(board == 0) 

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
