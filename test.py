import heuristic as ha
import unittest
import helper as help
import searchai as sa
import numpy as np
from parameterized import parameterized

# Case 8: Check monotonicity
optimal_board_01 = np.array([[128, 64, 32, 16],[0, 0, 0, 0],[0, 0, 0, 0],[0, 0, 0, 0]])
suboptimal_board_01 = np.array([[128, 32, 64, 16],[0, 0, 0, 0],[0, 0, 0, 0],[0, 0, 0, 0]])

sa.print_scores(optimal_board_01)
sa.print_scores(suboptimal_board_01)