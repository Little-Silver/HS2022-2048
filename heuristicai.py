import random
import game
import sys
import numpy as np

# Author:				chrn (original by nneonneo)
# Date:				    11.11.2016
# Description:			The logic of the AI to beat the game.

UP, DOWN, LEFT, RIGHT = 0, 1, 2, 3


def find_best_move(board):
    bestmove = -1

    # Build a heuristic agent on your own that is much better than the random agent.
    # Your own agent don't have to beat the game.
    print(board)

    bestmove = find_best_move_agent(board)
    return bestmove


def find_best_move_random_agent():
    return random.choice([UP, DOWN, LEFT, RIGHT])


def find_best_move_agent(board):
    current_zeros = np.count_nonzero(board == 0)
    simulation = np.array([
        simulate_move(board, UP, current_zeros),
        simulate_move(board, DOWN, current_zeros),
        simulate_move(board, LEFT, current_zeros),
        simulate_move(board, RIGHT, current_zeros)
    ])
    print(simulation)

    zeros = simulation[:, 1]
    goodness = simulation[:, 2]
    most_good_move = int(simulation[np.argmax(goodness), 0])
    most_zeros_move = int(simulation[np.argmax(zeros), 0])

    # TODO: include move goodness in move decision which move is best

    next_move = most_zeros_move

    return next_move


def simulate_move(board, move, current_zeros):
    new_board = board.copy()
    new_board = execute_move(move, new_board)
    zeros = np.count_nonzero(new_board == 0)

    zeros += find_alignment(board)

    if zeros >= current_zeros and not board_equals(new_board, board):
        return np.array([move, zeros, calculate_move_goodness(new_board)])
    return np.array([move, -1, -1])


# move goodness is increased if larger numbers have been combined
def calculate_move_goodness(board):
    non_zero_board = [x for x in board.flatten() if x != 0]
    return np.sum(np.log2(non_zero_board) ** 2)


def find_alignment(board):
    board_cp = board.copy()
    board_cp = board_cp[~np.all(board_cp == 0, axis=0)]
    board_cp = board_cp[~np.all(board_cp == 0, axis=1)]

    horizontal_alignments = 0
    vertical_alignments = 0

    # Check rows
    for i in range(0, len(board_cp)):
        horizontal_alignments = check_row(board_cp[i])

    # Check columns
    for i in range(0, len(board_cp[i])):
        vertical_alignments = check_row(board_cp[:, i])

    return max(horizontal_alignments, vertical_alignments)


def check_row(row):
    alignment = 0
    row = row[row != 0]
    previous = -1
    for i in range(0, len(row)):
        if (previous == row[i]):
            alignment += 1
            previous = -1
        else:
            previous = row[i]
    return alignment


def execute_move(move, board):
    """
    move and return the grid without a new random tile 
	It won't affect the state of the game in the browser.
    """

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
    return (newboard == board).all()
