#!/usr/bin/env python3
#
# Scrabble Game Tests
# Author: Chris Lyon
# Contact: chris@cplyon.ca

import logging
import sys
import unittest

from scrabb import Board


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


if __name__ == "__main__":
    logging.basicConfig(stream=sys.stderr)
    logging.getLogger().setLevel(logging.DEBUG)
    unittest.main()
