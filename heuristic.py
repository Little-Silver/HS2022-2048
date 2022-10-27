import numpy as np

BOARD_SIZE = 16

SCORE_TOP_LEFT = np.array([[2**15, 2**14, 2**13, 2**12], [2**8, 2**9, 2**10, 2**11], [2**7, 2**6, 2**5, 2**4], [0, 2**1, 2**2, 2**3]]) ** 2
SCORE_TOP_RIGHT = np.array([[2**12, 2**13, 2**14, 2**15], [2**11, 2**10, 2**9, 2**8], [2**4, 2**5, 2**6, 2**7], [2**3, 2**2, 2**1, 0]]) ** 2
SCORE_BOTTOM_LEFT = np.array([[0, 2**1, 2**2, 2**3], [2**7, 2**6, 2**5, 2**4], [2**8, 2**9, 2**10, 2**11], [2**15, 2**14, 2**13, 2**12]]) ** 2
SCORE_BOTTOM_RIGHT = np.array([[2**3, 2**2, 2**1, 0], [2**4, 2**5, 2**6, 2**7], [2**11, 2**10, 2**9, 2**8], [2**12, 2**13, 2**14, 2**15]]) ** 2

SCORE_BOARD_ARR = np.array([SCORE_TOP_LEFT, SCORE_TOP_RIGHT, SCORE_BOTTOM_LEFT, SCORE_BOTTOM_RIGHT])

def smoothness(board):
    #log_board = np.copy(board)
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
    return

def prioritize_edges(board):
    score_board = np.array([[2, 1, 1, 2],[1, 0, 0, 1], [1, 0, 0, 1], [2, 1, 1, 2]])
    return np.sum(np.power(score_board, board))