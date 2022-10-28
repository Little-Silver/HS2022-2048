import heuristic as ha
import unittest
import helper as help
import searchai as sa
import numpy as np
from parameterized import parameterized

# RUN: nosetests -v score_test.py

class TestBoards(unittest.TestCase):

    # Case 1: Optimal order
    optimal_board_01 = np.array([[128, 64, 32, 16],[0, 0, 0, 0],[0, 0, 0, 0],[0, 0, 0, 0]])
    suboptimal_board_01 = np.array([[128, 32, 64, 16],[0, 0, 0, 0],[0, 0, 0, 0],[0, 0, 0, 0]])

    # Case 2: High numbers in horizontal corners
    optimal_board_02 = np.array([[1024, 1024, 64, 16],[0, 0, 0, 0],[0, 0, 0, 0],[0, 0, 0, 0]])
    suboptimal_board_02 = np.array([[1024, 64, 32, 1024],[0, 0, 0, 0],[0, 0, 0, 0],[0, 0, 0, 0]])

    # Case 3: High numbers in diagonal corners
    optimal_board_03 = np.array([[1024, 32, 64, 16],[1024, 4, 2, 0],[0, 0, 0, 0],[0, 0, 0, 0]])
    suboptimal_board_03 = np.array([[1024, 64, 32, 16],[4, 2, 0, 0],[0, 0, 0, 0],[0, 0, 0, 1024]])

    # Case 4: 
    optimal_board_04 = np.array([[0, 32, 64, 64],[0, 0, 4, 8],[0, 2, 0, 0],[0, 0, 0, 2]])
    suboptimal_board_04 = np.array([[32, 64, 32, 32],[4, 2, 4, 4],[0, 2, 0, 0],[0, 0, 0, 0]])


    @parameterized.expand([
        [optimal_board_01, suboptimal_board_01, 1],
        [optimal_board_02, suboptimal_board_02, 2],
        [optimal_board_03, suboptimal_board_03, 3],
        [optimal_board_04, suboptimal_board_04, 4],
    ])
    def test_boards(self, b1, b2, i):    
        score_optimal = sa.score_board(b1)
        score_suboptimal = sa.score_board(b2)
        msg = "\nCase {0}: \nBoard 1 (Score = {1}): \n{2} \nBoard 2 (Score = {3}): \n{4}".format(i, score_optimal, b1, score_suboptimal, b2)
        self.assertTrue(score_optimal > score_suboptimal, msg)

if __name__ == '__main__':
    unittest.main()