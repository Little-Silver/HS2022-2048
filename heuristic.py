import numpy as np
from numba import njit

BOARD_SIZE = 16
BOARD_WIDTH = 4
BOARD_HEIGHT = 4


# The difference between adjacent tiles should be rather low
def smoothness(board):
    hor = 1 + np.sum(np.abs(np.diff(board, axis=1)))
    ver = 1 + np.sum(np.abs(np.diff(board, axis=0)))
    return max(0, 2*np.sum(board) - ((ver + hor)/2))


# It is optimal to have the board aligned in a snake form (from highest to lowest tile)
def snake_score(board):
    snake = np.zeros(8)

    for row in range(BOARD_WIDTH):

        for col in range(BOARD_HEIGHT - 1):
            if (row % 2 == 0):
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


def snake_score_variant(board):
    snake_array = np.array([]).reshape(1, 8)
    # top left to bottom right (horizontal)
    snake_array[0] = np.array([board[0], np.flip(board[1]), board[2], np.flip(board[3])]).flatten()
    # bottom right to top left (horizontal)
    snake_array[1] = np.flip(snake_array[0].copy())
    # top right to bottom left (horizontal)
    snake_array[2] = np.array([np.flip(board[0]), board[1], np.flip(board[2]), board[3]]).flatten()
    # bottom left to bottom right (horizontal)
    snake_array[3] = np.flip(snake_array[2].copy())

    # top left to bottom right (vertical)
    snake_array[4] = np.array([board[:, 0], np.flip(board[:, 1]), board[:, 2], np.flip(board[:, 3])]).flatten()
    # bottom right to top left (vertical)
    snake_array[5] = np.flip(snake_array[4].copy())
    # top right to bottom left (vertical)
    snake_array[6] = np.array([np.flip(board[:, 0]), board[:, 1], np.flip(board[:, 2]), board[:, 3]]).flatten()
    # bottom left to bottom right (vertical)
    snake_array[7] = np.flip(snake_array[6].copy())

    score = np.array([]).reshape(8)
    for i in range(8):
        score[i] = length_longest_descending_sequence(snake_array[i])

    return np.max(score)


# returns length of the longest descending sequence in array
def length_longest_descending_sequence(array):
    length = 0
    max_length = 0
    for i in range(len(array) - 1):
        if array[i + 1] > array[i]:
            max_length = length
            length = 0
        else:
            length += 1
    return max(length, max_length)


# Helper function
def count_zeros(board):
    return 16 - np.count_nonzero(board)


# Having more zeros is better than having few
def zero_penalty(board):
    zeros = count_zeros(board)
    penalty = np.array([0.43, 0.53, 0.64, 0.72, 0.79, 0.85, 0.9, 0.94, 0.97, 0.99, 1, 1, 1, 1, 1, 1])
    return penalty[zeros]

# High tiles should remain in corners or edges
def prioritize_edges(board):
    score_board = np.array([[3, 2, 2, 3], [2, 0, 0, 2], [2, 0, 0, 2], [3, 2, 2, 3]])
    return np.sum(np.multiply(score_board, board)) / 100

def highest_tile(board):
    highest_corners = max(board[0,0],board[0,3],board[3,0],board[3,3])
    highest_tile = np.max(board)
    if (highest_tile == highest_corners):
        return np.log2(highest_tile)
    else:
        return 0

# Values going from one corner to an oposing corner should all be either increasing or decreasing
#@njit
def monotonicity(board):
    mono = 0

    for r in board:
        if r[0] < r[1]:
            diff = 1
        else:
            diff = -1
        for i in range(BOARD_WIDTH - 1):
            if (r[i] - r[i + 1]) * diff <= 0:
                mono += 1
            if r[i] < r[i+1]:
                diff = 1
            else:
                diff = -1
    print(mono)
    for j in range(4):
        if board[0][j] < board[1][j]:
            diff = 1
        else:
            diff = -1
        for k in range(BOARD_HEIGHT - 1):
            if (board[k][j] - board[k + 1][j]) * diff <= 0:
                mono += 1
            if board[k][j] < board[k + 1][j]:
                diff = 1
            else:
                diff = -1            
    print(mono)
    return mono
