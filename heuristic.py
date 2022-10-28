import numpy as np

BOARD_SIZE = 16

SCORE_TOP_LEFT = np.array([[15, 14, 13, 12], [8, 9, 10, 11], [7, 6, 5, 4], [0, 1, 2, 3]]) ** 2
SCORE_TOP_RIGHT = np.array([[12, 13, 14, 15], [11, 10, 9, 8], [4, 5, 6, 7], [3, 2, 1, 0]]) ** 2
SCORE_BOTTOM_LEFT = np.array([[0, 1, 2, 3], [7, 6, 5, 4], [8, 9, 10, 11], [15, 14, 13, 12]]) ** 2
SCORE_BOTTOM_RIGHT = np.array([[3, 2, 1, 0], [4, 5, 6, 7], [11, 10, 9, 8], [12, 13, 14, 15]]) ** 2

SCORE_BOARD_ARR = np.array([SCORE_TOP_LEFT, SCORE_TOP_RIGHT, SCORE_BOTTOM_LEFT, SCORE_BOTTOM_RIGHT])

def smoothness(board):
    ver = 1
    hor = 1
    for i in range(3):
        ver += np.sum(abs(board[i] - board[i+1]))
        hor += np.sum(abs(board[:,i] - board[:,i+1]))
    return (1/(min(ver, hor)**2))

def weighted_board_score(board):
    s_max = 0
    for SCORE_BOARD in SCORE_BOARD_ARR:
        s_max = max(np.sum(np.multiply(board, SCORE_BOARD)), s_max)
    return s_max

def count_zeros(board):
    return (16 - np.count_nonzero(board))

def zero_penalty(board):
    zeros = count_zeros(board)
    penalty = np.array([0.43, 0.53, 0.64, 0.72, 0.79, 0.85, 0.9, 0.94, 0.97, 0.99, 1, 1, 1, 1, 1, 1])
    return penalty[zeros]

def prioritize_edges(board):
    score_board = np.array([[3, 2, 2, 3],[2, 0, 0, 2], [2, 0, 0, 2], [3, 2, 2, 3]])
    return np.sum(np.power(score_board, board))