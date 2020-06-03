#!/usr/bin/env python3
#
# Scrabble Game Tests
# Author: Chris Lyon
# Contact: chris@cplyon.ca

import logging
import sys
import unittest

from scrabb import Board
from scrabb import Letter


class GameTest(unittest.TestCase):
    def setUp(self):
        pass

    def test_validate_middle_true(self):
        board = Board()
        is_valid = board.is_valid_play(
            [Board.MIDDLE,
            (Board.MIDDLE[0], Board.MIDDLE[1] + 1),
            (Board.MIDDLE[0], Board.MIDDLE[1] + 2)])

        self.assertTrue(is_valid)

    def test_validate_middle_false(self):
        board = Board()
        is_valid = board.is_valid_play(
            [(Board.MIDDLE[0], Board.MIDDLE[1] + 1),
            (Board.MIDDLE[0], Board.MIDDLE[1] + 2)])

        self.assertFalse(is_valid)

    def test_validate_cell_full(self):
        board = Board()
        board._board[Board.MIDDLE[0]][Board.MIDDLE[1]] = Letter('A', 1)
        is_valid = board.is_valid_play([Board.MIDDLE])
        self.assertFalse(is_valid)

    def test_not_in_same_row(self):
        board = Board()
        is_valid = board.is_valid_play(
            [Board.MIDDLE,
            (Board.MIDDLE[0], Board.MIDDLE[1] + 1),
            (Board.MIDDLE[0]+1, Board.MIDDLE[1] + 2)])
        self.assertFalse(is_valid)

    def test_not_in_same_column(self):
        board = Board()
        is_valid = board.is_valid_play(
            [Board.MIDDLE,
            (Board.MIDDLE[0]+1, Board.MIDDLE[1]),
            (Board.MIDDLE[0]+2, Board.MIDDLE[1] + 1)])
        self.assertFalse(is_valid)

    def test_horizonal_noncontiguous(self):
        board = Board()
        is_valid = board.is_valid_play(
            [Board.MIDDLE,
            (Board.MIDDLE[0], Board.MIDDLE[1] + 1),
            (Board.MIDDLE[0], Board.MIDDLE[1] + 3)])
        self.assertFalse(is_valid)

    def test_vertical_noncontiguous(self):
        board = Board()
        is_valid = board.is_valid_play(
            [Board.MIDDLE,
            (Board.MIDDLE[0]+1, Board.MIDDLE[1]),
            (Board.MIDDLE[0]+3, Board.MIDDLE[1])])
        self.assertFalse(is_valid)

    def test_validate_not_touching(self):
        board = Board()
        board._board[Board.MIDDLE[0]][Board.MIDDLE[1]] = Letter('A', 1)
        board.is_empty = False
        is_valid = board.is_valid_play([(Board.MIDDLE[0], Board.MIDDLE[1]+4)])
        self.assertFalse(is_valid)

if __name__ == "__main__":
    logging.basicConfig(stream=sys.stderr)
    logging.getLogger().setLevel(logging.DEBUG)
    unittest.main()
