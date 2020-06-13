#!/usr/bin/env python3
#
# Scrabble Game Tests
# Author: Chris Lyon
# Contact: chris@cplyon.ca

import logging
import sys
import unittest

from scrabb.scrabb import Board
from scrabb.scrabb import Letter
from scrabb.scrabb import Orientation


class BoardTest(unittest.TestCase):
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

    def test_validate_touching_left(self):
        board = Board()
        board._board[Board.MIDDLE[0]][Board.MIDDLE[1]] = Letter('A', 1)
        board.is_empty = False
        is_valid = board.is_valid_play([(Board.MIDDLE[0], Board.MIDDLE[1]-1)])
        self.assertTrue(is_valid)

    def test_validate_touching_right(self):
        board = Board()
        board._board[Board.MIDDLE[0]][Board.MIDDLE[1]] = Letter('A', 1)
        board.is_empty = False
        is_valid = board.is_valid_play([(Board.MIDDLE[0], Board.MIDDLE[1]+1)])
        self.assertTrue(is_valid)

    def test_validate_touching_above(self):
        board = Board()
        board._board[Board.MIDDLE[0]][Board.MIDDLE[1]] = Letter('A', 1)
        board.is_empty = False
        is_valid = board.is_valid_play([(Board.MIDDLE[0]+1, Board.MIDDLE[1])])
        self.assertTrue(is_valid)

    def test_validate_touching_below(self):
        board = Board()
        board._board[Board.MIDDLE[0]][Board.MIDDLE[1]] = Letter('A', 1)
        board.is_empty = False
        is_valid = board.is_valid_play([(Board.MIDDLE[0]-1, Board.MIDDLE[1])])
        self.assertTrue(is_valid)

    def test_get_orientation_single(self):
        board = Board()
        orientation = board.get_orientation([Board.MIDDLE])
        self.assertEqual(orientation, Orientation.HORIZONTAL)

    def test_get_orientation_horizontal(self):
        board = Board()
        orientation = board.get_orientation([Board.MIDDLE, (Board.MIDDLE[0], Board.MIDDLE[1]+1)])
        self.assertEqual(orientation, Orientation.HORIZONTAL)

    def test_get_orientation_vertical(self):
        board = Board()
        orientation = board.get_orientation([Board.MIDDLE, (Board.MIDDLE[0]+1, Board.MIDDLE[1])])
        self.assertEqual(orientation, Orientation.VERTICAL)

    def test_get_orientation_none(self):
        board = Board()
        orientation = board.get_orientation([Board.MIDDLE, (Board.MIDDLE[0]+1, Board.MIDDLE[1]+1)])
        self.assertEqual(orientation, Orientation.NONE)


if __name__ == "__main__":
    logging.basicConfig(stream=sys.stderr)
    logging.getLogger().setLevel(logging.DEBUG)
    unittest.main()
