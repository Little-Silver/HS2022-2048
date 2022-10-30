import numpy as np

BOARD_SIZE = 16
BOARD_WIDTH = 4
BOARD_HEIGHT = 4

SCORE_TOP_LEFT = np.array([[15, 14, 13, 12], [8, 9, 10, 11], [7, 6, 5, 4], [0, 1, 2, 3]])
SCORE_TOP_RIGHT = np.array([[12, 13, 14, 15], [11, 10, 9, 8], [4, 5, 6, 7], [3, 2, 1, 0]])
SCORE_BOTTOM_LEFT = np.array([[0, 1, 2, 3], [7, 6, 5, 4], [8, 9, 10, 11], [15, 14, 13, 12]])
SCORE_BOTTOM_RIGHT = np.array([[3, 2, 1, 0], [4, 5, 6, 7], [11, 10, 9, 8], [12, 13, 14, 15]])

SCORE_BOARD_ARR = np.array([SCORE_TOP_LEFT, SCORE_TOP_RIGHT, SCORE_BOTTOM_LEFT, SCORE_BOTTOM_RIGHT])

HIGH_VALUE = 100


# The difference between adjacent tiles should be rather low
def smoothness(board):
    ver = 0
    hor = 0
    for i in range(3):
        ver += np.sum(abs(board[i] - board[i + 1]))
        hor += np.sum(abs(board[:, i] - board[:, i + 1]))
    return min(ver, hor)


# It is optimal to have the board aligned in a snake form (from highest to lowest tile)
def snake_score(board):
    snake = np.zeros((8))

    for row in range(BOARD_WIDTH):

        for col in range(BOARD_HEIGHT - 1):
            if (row%2 == 0): 
                if (board[row, col] < board[row, col + 1]):
                    snake[0] += 1
                if (board[col, row] < board[col + 1, row]):
                    snake[1] += 1
                if (board[row, col] > board[row, col + 1]):
                    snake[2] += 1
                if (board[col, row] > board[col + 1, row]):
                    snake[3] += 1
                if (board[row, -1 - col] < board[row, -2 - col]):
                    snake[4] += 1
                if (board[-1 - col, row] < board[-2 - col, row]):
                    snake[5] += 1  
                if (board[row, -1 - col] > board[row, -2 - col]):
                    snake[6] += 1
                if (board[-1 - col, row] > board[-2 - col, row]):
                    snake[7] += 1 
            else:
                if (board[row, -1 - col] < board[row, -2 - col]):
                    snake[0] += 1
                if (board[-1 - col, row] < board[-2 - col, row]):
                    snake[1] += 1  
                if (board[row, -1 - col] > board[row, -2 - col]):
                    snake[2] += 1
                if (board[-1 - col, row] > board[-2 - col, row]):
                    snake[3] += 1  
                if (board[row, col] < board[row, col + 1]):
                    snake[4] += 1
                if (board[col, row] < board[col + 1, row]):
                    snake[5] += 1
                if (board[row, col] > board[row, col + 1]):
                    snake[6] += 1
                if (board[col, row] > board[col + 1, row]):
                    snake[7] += 1

    return np.min(snake)

# Helper function
def count_zeros(board):
    return 16 - np.count_nonzero(board)

# Having more zeros is better than having few
def zero_penalty(board):
    zeros = count_zeros(board)
    penalty = np.array([1, 0.7, 0.5, 0.3, 0.2, 0.15, 0.1, 0.05, 0, 0, 0, 0, 0, 0, 0, 0])
    return penalty[zeros]

# High tiles should remain in corners or edges
def prioritize_edges(board):
    score_board = np.array([[0, 1e-3, 1e-3, 0],[1e-3, 1e-2, 1e-2, 1e-3], [1e-3, 1e-2, 1e-2, 1e-3], [0, 1e-3, 1e-3, 0]])
    return np.sum(np.multiply(score_board, board))

# Values going from one corner to an oposing corner should all be either increasing or decreasing
def monotonicity(board):
    mono = 24

    for r in board:
        if (r[0] < r[1]): diff = 1
        else: diff = -1
        for i in range(BOARD_WIDTH - 1):
            if (r[i] - r[i + 1]) * diff <= 0:
                mono -= 1
            diff = r[i] - r[i + 1]

    for j in range(4):
        if (board[0][j] < board[1][j]): diff = 1
        else: diff = -1
        for k in range(BOARD_HEIGHT - 1):
            if (board[k][j] - board[k + 1][j]) * diff <= 0:
                mono -= 1
            diff = board[k][j] - board[k + 1][j]

    return mono
