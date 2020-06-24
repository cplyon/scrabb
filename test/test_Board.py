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
from scrabb.scrabb import ValidationReason


class BoardTest(unittest.TestCase):
    def setUp(self):
        pass

    # Validation Tests
    def test_validate_middle_true(self):
        board = Board()
        is_valid = board.is_valid_play(
            [Board.MIDDLE,
                (Board.MIDDLE[0], Board.MIDDLE[1] + 1),
                (Board.MIDDLE[0], Board.MIDDLE[1] + 2)])
        self.assertEqual(is_valid, ValidationReason.VALID)

    def test_validate_middle_false(self):
        board = Board()
        is_valid = board.is_valid_play(
            [(Board.MIDDLE[0], Board.MIDDLE[1] + 1),
                (Board.MIDDLE[0], Board.MIDDLE[1] + 2)])
        self.assertEqual(is_valid,
                         ValidationReason.FIRST_PLAY_NOT_ON_MIDDLE_CELL)

    def test_validate_first_play_too_short(self):
        board = Board()
        board._board[Board.MIDDLE[0]][Board.MIDDLE[1]] = Letter('A', 1)
        is_valid = board.is_valid_play([Board.MIDDLE])
        self.assertEqual(is_valid,
                         ValidationReason.FIRST_PLAY_TOO_FEW_TILES)

    def test_validate_cell_full(self):
        board = Board()
        board._board[Board.MIDDLE[0]][Board.MIDDLE[1]] = Letter('A', 1)
        board.is_empty = False
        is_valid = board.is_valid_play([Board.MIDDLE])
        self.assertEqual(is_valid,
                         ValidationReason.CELL_ALREADY_FULL)

    def test_validate_not_in_same_row(self):
        board = Board()
        is_valid = board.is_valid_play(
            [Board.MIDDLE,
                (Board.MIDDLE[0], Board.MIDDLE[1] + 1),
                (Board.MIDDLE[0]+1, Board.MIDDLE[1] + 2)])
        self.assertEqual(is_valid,
                         ValidationReason.INVALID_ORIENTATION)

    def test_validate_not_in_same_column(self):
        board = Board()
        is_valid = board.is_valid_play(
            [Board.MIDDLE,
                (Board.MIDDLE[0]+1, Board.MIDDLE[1]),
                (Board.MIDDLE[0]+2, Board.MIDDLE[1] + 1)])
        self.assertEqual(is_valid,
                         ValidationReason.INVALID_ORIENTATION)

    def test_validate_noncontiguous_horizontal(self):
        board = Board()
        is_valid = board.is_valid_play(
            [Board.MIDDLE,
                (Board.MIDDLE[0], Board.MIDDLE[1] + 1),
                (Board.MIDDLE[0], Board.MIDDLE[1] + 3)])
        self.assertEqual(is_valid,
                         ValidationReason.NOT_ALL_CONNECTED)

    def test_validate_noncontiguous_vertical(self):
        board = Board()
        is_valid = board.is_valid_play(
            [Board.MIDDLE,
                (Board.MIDDLE[0]+1, Board.MIDDLE[1]),
                (Board.MIDDLE[0]+3, Board.MIDDLE[1])])
        self.assertEqual(is_valid,
                         ValidationReason.NOT_ALL_CONNECTED)

    def test_validate_not_touching(self):
        board = Board()
        board._board[Board.MIDDLE[0]][Board.MIDDLE[1]] = Letter('A', 1)
        board.is_empty = False
        is_valid = board.is_valid_play([(Board.MIDDLE[0], Board.MIDDLE[1]+4)])
        self.assertEqual(is_valid,
                         ValidationReason.NOT_TOUCHING_EXISTING)

    def test_validate_touching_left(self):
        board = Board()
        board._board[Board.MIDDLE[0]][Board.MIDDLE[1]] = Letter('A', 1)
        board.is_empty = False
        is_valid = board.is_valid_play([(Board.MIDDLE[0], Board.MIDDLE[1]-1)])
        self.assertEqual(is_valid, ValidationReason.VALID)

    def test_validate_touching_right(self):
        board = Board()
        board._board[Board.MIDDLE[0]][Board.MIDDLE[1]] = Letter('A', 1)
        board.is_empty = False
        is_valid = board.is_valid_play([(Board.MIDDLE[0], Board.MIDDLE[1]+1)])
        self.assertEqual(is_valid, ValidationReason.VALID)

    def test_validate_touching_above(self):
        board = Board()
        board._board[Board.MIDDLE[0]][Board.MIDDLE[1]] = Letter('A', 1)
        board.is_empty = False
        is_valid = board.is_valid_play([(Board.MIDDLE[0]+1, Board.MIDDLE[1])])
        self.assertEqual(is_valid, ValidationReason.VALID)

    def test_validate_touching_below(self):
        board = Board()
        board._board[Board.MIDDLE[0]][Board.MIDDLE[1]] = Letter('A', 1)
        board.is_empty = False
        is_valid = board.is_valid_play([(Board.MIDDLE[0]-1, Board.MIDDLE[1])])
        self.assertEqual(is_valid, ValidationReason.VALID)

    def test_validate_prefix_suffix_horizontal(self):
        board = Board()
        board._board[Board.MIDDLE[0]][Board.MIDDLE[1]] = Letter('A', 1)
        board.is_empty = False
        is_valid = board.is_valid_play([(Board.MIDDLE[0], Board.MIDDLE[1]-1),
                                        (Board.MIDDLE[0], Board.MIDDLE[1]+1)])
        self.assertEqual(is_valid, ValidationReason.VALID)

    def test_validate_prefix_suffix_vertical(self):
        board = Board()
        board._board[Board.MIDDLE[0]][Board.MIDDLE[1]] = Letter('A', 1)
        board.is_empty = False
        is_valid = board.is_valid_play([(Board.MIDDLE[0]-1, Board.MIDDLE[1]),
                                        (Board.MIDDLE[0]+1, Board.MIDDLE[1])])
        self.assertEqual(is_valid, ValidationReason.VALID)

    # Get Orientation Tests
    def test_get_orientation_single(self):
        board = Board()
        orientation = board.get_orientation([Board.MIDDLE])
        self.assertEqual(orientation, Orientation.HORIZONTAL)

    def test_get_orientation_horizontal(self):
        board = Board()
        orientation = board.get_orientation([Board.MIDDLE,
                                             (Board.MIDDLE[0],
                                              Board.MIDDLE[1]+1)])
        self.assertEqual(orientation, Orientation.HORIZONTAL)

    def test_get_orientation_vertical(self):
        board = Board()
        orientation = board.get_orientation([Board.MIDDLE,
                                             (Board.MIDDLE[0]+1,
                                              Board.MIDDLE[1])])
        self.assertEqual(orientation, Orientation.VERTICAL)

    def test_get_orientation_none(self):
        board = Board()
        orientation = board.get_orientation([Board.MIDDLE,
                                             (Board.MIDDLE[0]+1,
                                              Board.MIDDLE[1]+1)])
        self.assertEqual(orientation, Orientation.NONE)


if __name__ == "__main__":
    logging.basicConfig(stream=sys.stderr)
    logging.getLogger().setLevel(logging.DEBUG)
    unittest.main()
