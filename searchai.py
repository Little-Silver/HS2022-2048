import numpy as np
import multiprocessing
from itertools import product
import heuristic as ha
import helper as help

# Author:      chrn (original by nneonneo)
# Date:        11.11.2016
# Copyright:   Algorithm from https://github.com/nneonneo/2048-ai
# Description: The logic to beat the game. Based on expectimax algorithm.

BOARD_WIDTH = 4
BOARD_HEIGHT = 4

UP, DOWN, LEFT, RIGHT = 0, 1, 2, 3

# ********************************* MAIN *********************************
def find_best_move(board):
    bestmove = -1
    UP, DOWN, LEFT, RIGHT = 0, 1, 2, 3
    move_args = [UP,DOWN,LEFT,RIGHT]

    input("Next? ")

    result = [score_toplevel_move(i, board) for i in range(len(move_args))]
    bestmove = result.index(min(result))

    for m in move_args:
        if m == UP: 
            print_scores(board)
            print(board)
        print("move: %d score: %.4f" % (m, result[m]))
    return bestmove

def score_toplevel_move(move, board):

    zeros = ha.count_zeros(board)
    
    depth = 1
    if(zeros < 4):
        depth = 2
    if (zeros < 2):
        depth = 3

    return step(board, move, depth, 1)

# ********************************* EXPECTIMAX *********************************
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

def step(board, move, depth, prob):
    new_board = help.execute_move(move, board)
    if help.board_equals(board, new_board):
        return 10000
    else:
        return score_spawn_possibilities(new_board, depth, prob)

def simulate_move(board, depth, probability):

    if depth == 0:
        return probability * score_board(board)
    
    depth -= 1
    
    score_up = step(board, UP, depth, probability)
    score_left = step(board, LEFT, depth, probability)
    score_right = step(board, RIGHT, depth, probability)
    score_down = step(board, DOWN, depth, probability)

    return min(score_up, score_down, score_left, score_right)

# ********************************* SCORING *********************************
FACTOR_EMPTY_TILES = 1
FACTOR_SMOOTHNESS = 1
FACTOR_EDGES = 5
FACTOR_BOARD_WEIGHT = 1

def score_board(board):
    zeros, smooth, weight, g = score(board)
    return (weight + g) * zeros * smooth

def score(board):
    #board[np.where(board == 0)] = 1
    board_log = board#np.log2(board)
    zeros = ha.zero_penalty(board_log) ** FACTOR_EMPTY_TILES
    smooth = ha.smoothness(board_log)/FACTOR_SMOOTHNESS
    snake = FACTOR_EDGES*ha.snake_score(board_log)
    edge_priority = FACTOR_BOARD_WEIGHT*ha.prioritize_edges(board_log)
    return zeros, smooth, snake, edge_priority

def print_scores(board):
    zeros, smooth, snake, edge_priority = score(board)
    total = score_board(board)
    print(f"total: {total}, zeros: {zeros}, smooth: {smooth}, snake: {snake}, edges: {edge_priority}")
