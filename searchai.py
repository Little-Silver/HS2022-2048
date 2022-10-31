import numpy as np
import heuristic as ha
import helper as help

# Author:      chrn (original by nneonneo)
# Date:        11.11.2016
# Copyright:   Algorithm from https://github.com/nneonneo/2048-ai
# Description: The logic to beat the game. Based on expectimax algorithm.

BOARD_WIDTH = 4
BOARD_HEIGHT = 4

UP, DOWN, LEFT, RIGHT = 0, 1, 2, 3

MIN_PROB = 0.0005


# ********************************* MAIN *********************************
def find_best_move(board):
    bestmove = -1
    move_args = [UP, DOWN, LEFT, RIGHT]

    # input("Next? ")

    result = [score_toplevel_move(i, board) for i in range(len(move_args))]
    bestmove = result.index(max(result))

    for m in move_args:
        if m == UP:
            print_scores(board)
            print(board)
        print("move: %d score: %.4f" % (m, result[m]))
    return bestmove


def score_toplevel_move(move, board):
    zeros = ha.count_zeros(board)

    depth = 2
    if (zeros < 2):
        depth = 3
    if (zeros < 0):
        depth = 4

    return step(board, move, depth, 1)


# ********************************* EXPECTIMAX *********************************
def score_spawn_possibilities(board, depth, prob):
    zeros = ha.count_zeros(board)
    prob_2 = 0.9 / zeros
    prob_4 = 0.1 / zeros
   
    score = 10 + np.sum(np.array([
        simulate_move(x, y, 2, board, depth, prob * prob_2) + 
        simulate_move(x, y, 4, board, depth, prob * prob_4)
        for (x,y), val in np.ndenumerate(board) if val == 0
        ]))

    return score


def step(board, move, depth, prob):
    new_board = help.execute_move(move, board)
    if help.board_equals(board, new_board):
        return 0
    else:
        return score_spawn_possibilities(new_board, depth, prob)


def simulate_move(x, y, val, board, depth, probability):
    board = np.copy(board)
    board[x][y] = val
    if depth == 0 or probability <= MIN_PROB:
        return probability * score_board(board)

    depth -= 1

    score_up = step(board, UP, depth, probability)
    score_left = step(board, LEFT, depth, probability)
    score_right = step(board, RIGHT, depth, probability)
    score_down = step(board, DOWN, depth, probability)

    return max(score_up, score_down, score_left, score_right)


# ********************************* SCORING *********************************
FACTOR_EMPTY_TILES = 3
FACTOR_SMOOTHNESS = 0.1
FACTOR_EDGES = 1
FACTOR_SNAKE = 1
FACTOR_MONO = 3
FACTOR_HIGHEST = 4

def score_board(board):
    zeros, smooth, snake, edge_priority, monotonicity, highest_tile = score(board)
    return monotonicity + zeros  + highest_tile+ edge_priority + smooth#+ snake + smooth

def score(board):
    zeros = 0#FACTOR_EMPTY_TILES*ha.zero_penalty(board)
    smooth = FACTOR_SMOOTHNESS*ha.smoothness(board)
    snake = 0#FACTOR_SNAKE*ha.snake_score(board)
    edge_priority =0#FACTOR_EDGES*ha.prioritize_edges(board)
    monotonicity = 0#FACTOR_MONO*ha.monotonicity(board)
    highest_tile = 0#FACTOR_HIGHEST*ha.highest_tile(board)
    return zeros, smooth, snake, edge_priority, monotonicity, highest_tile


def print_scores(board):
    zeros, smooth, snake, edge_priority, monotonicity, highest_tile = score(board)
    total = score_board(board)
    print(f"total: {total}, zeros: {zeros}, smooth: {smooth}, snake: {snake}, edges: {edge_priority}, mono: {monotonicity}, highest_tile: {highest_tile}")
