#!/usr/bin/env python3
#
# Scrabble Game Tests
# Author: Chris Lyon
# Contact: chris@cplyon.ca

import unittest

from scrabb.board import Board
from scrabb.letter import Letter
from scrabb.scrabb import Game
from scrabb.scrabb import InvalidPlayException
from scrabb.scrabb import Orientation
from scrabb.scrabb import AdjacentDirection
from scrabb.scrabb import ValidationReason


class GameTest(unittest.TestCase):

    def setUp(self):
        pass

    # Validation Tests
    def test_is_valid_invalid_orientation(self):
        game = Game()
        is_valid = game.is_valid_play(
            [Board.MIDDLE,
                (Board.MIDDLE[0], Board.MIDDLE[1] + 1),
                (Board.MIDDLE[0]+1, Board.MIDDLE[1] + 1)],
            Orientation.NONE)
        self.assertEqual(is_valid, ValidationReason.INVALID_ORIENTATION)

    def test_is_valid_horizontal_true(self):
        game = Game()
        is_valid = game.is_valid_play(
            [Board.MIDDLE,
                (Board.MIDDLE[0], Board.MIDDLE[1] + 1),
                (Board.MIDDLE[0], Board.MIDDLE[1] + 2)],
            Orientation.HORIZONTAL)
        self.assertEqual(is_valid, ValidationReason.VALID)

    def test_is_valid_vertical_true(self):
        game = Game()
        is_valid = game.is_valid_play(
            [Board.MIDDLE,
                (Board.MIDDLE[0] + 1, Board.MIDDLE[1]),
                (Board.MIDDLE[0] + 2, Board.MIDDLE[1])],
            Orientation.VERTICAL)
        self.assertEqual(is_valid, ValidationReason.VALID)

    def test_is_valid_first_play_not_on_middle(self):
        game = Game()
        is_valid = game.is_valid_play(
            [(Board.MIDDLE[0], Board.MIDDLE[1] + 1),
                (Board.MIDDLE[0], Board.MIDDLE[1] + 2)],
            Orientation.HORIZONTAL)
        self.assertEqual(is_valid,
                         ValidationReason.FIRST_PLAY_NOT_ON_MIDDLE_CELL)

    def test_is_valid_first_play_too_short(self):
        game = Game()
        game.board[Board.MIDDLE[0]][Board.MIDDLE[1]] = Letter('A', 1)
        is_valid = game.is_valid_play([Board.MIDDLE], Orientation.HORIZONTAL)
        self.assertEqual(is_valid,
                         ValidationReason.FIRST_PLAY_TOO_FEW_TILES)

    def test_is_valid_cell_full(self):
        game = Game()
        game.board[Board.MIDDLE[0]][Board.MIDDLE[1]] = Letter('A', 1)
        game.board.is_empty = False
        is_valid = game.is_valid_play([Board.MIDDLE], Orientation.HORIZONTAL)
        self.assertEqual(is_valid,
                         ValidationReason.CELL_ALREADY_FULL)

    def test_is_valid_not_adjacent(self):
        game = Game()
        game.board[Board.MIDDLE[0]][Board.MIDDLE[1]] = Letter('A', 1)
        game.board.is_empty = False
        is_valid = game.is_valid_play([(Board.MIDDLE[0]+5, Board.MIDDLE[1])],
                                      Orientation.HORIZONTAL)
        self.assertEqual(is_valid,
                         ValidationReason.NOT_ADJACENT)

    def test_is_valid_noncontiguous_horizontal(self):
        game = Game()
        is_valid = game.is_valid_play(
            [Board.MIDDLE,
                (Board.MIDDLE[0], Board.MIDDLE[1] + 1),
                (Board.MIDDLE[0], Board.MIDDLE[1] + 3)],
            Orientation.HORIZONTAL)
        self.assertEqual(is_valid,
                         ValidationReason.NOT_CONTIGUOUS)

    def test_is_valid_noncontiguous_vertical(self):
        game = Game()
        is_valid = game.is_valid_play(
            [Board.MIDDLE,
                (Board.MIDDLE[0]+1, Board.MIDDLE[1]),
                (Board.MIDDLE[0]+3, Board.MIDDLE[1])],
            Orientation.VERTICAL)
        self.assertEqual(is_valid,
                         ValidationReason.NOT_CONTIGUOUS)

    def test_is_valid_prefix_suffix_horizontal(self):
        game = Game()
        game.board[Board.MIDDLE[0]][Board.MIDDLE[1]] = Letter('A', 1)
        game.board.is_empty = False
        is_valid = game.is_valid_play([(Board.MIDDLE[0], Board.MIDDLE[1]-1),
                                       (Board.MIDDLE[0], Board.MIDDLE[1]+1)],
                                      Orientation.HORIZONTAL)
        self.assertEqual(is_valid, ValidationReason.VALID)

    def test_is_valid_prefix_suffix_vertical(self):
        game = Game()
        game.board[Board.MIDDLE[0]][Board.MIDDLE[1]] = Letter('A', 1)
        game.board.is_empty = False
        is_valid = game.is_valid_play([(Board.MIDDLE[0]-1, Board.MIDDLE[1]),
                                      (Board.MIDDLE[0]+1, Board.MIDDLE[1])],
                                      Orientation.VERTICAL)
        self.assertEqual(is_valid, ValidationReason.VALID)

    # Get Orientation Tests
    def test_get_orientation_single(self):
        game = Game()
        orientation = game.get_orientation([Board.MIDDLE])
        self.assertEqual(orientation, Orientation.HORIZONTAL)

    def test_get_orientation_horizontal(self):
        game = Game()
        orientation = game.get_orientation([Board.MIDDLE,
                                            (Board.MIDDLE[0],
                                             Board.MIDDLE[1]+1)])
        self.assertEqual(orientation, Orientation.HORIZONTAL)

    def test_get_orientation_vertical(self):
        game = Game()
        orientation = game.get_orientation([Board.MIDDLE,
                                            (Board.MIDDLE[0]+1,
                                             Board.MIDDLE[1])])
        self.assertEqual(orientation, Orientation.VERTICAL)

    def test_get_orientation_none(self):
        game = Game()
        orientation = game.get_orientation([Board.MIDDLE,
                                            (Board.MIDDLE[0]+1,
                                             Board.MIDDLE[1]+1)])
        self.assertEqual(orientation, Orientation.NONE)

    # Play Letters Tests
    def test_play_letters_invalid(self):
        position = (Board.MIDDLE[0], Board.MIDDLE[1]+4)
        game = Game()
        with self.assertRaises(InvalidPlayException) as e:
            game.play_letters(
                {position: Letter('A', 1)})
            self.assertEqual(e.positions, [position])
            self.assertEqual(e.orientation, Orientation.HORIZONTAL)
            self.assertEqual(e.valid_reason,
                             ValidationReason.FIRST_PLAY_TOO_FEW_TILES)

    # Is Adjacent Tests
    def test_is_adjacent_none(self):
        game = Game()
        game.board[Board.MIDDLE[0]][Board.MIDDLE[1]] = Letter('A', 1)
        game.board.is_empty = False
        direction = game.is_adjacent((Board.MIDDLE[0], Board.MIDDLE[1]+4))
        self.assertEqual(direction, AdjacentDirection.NONE)

    def test_is_adjacent_left(self):
        game = Game()
        game.board[Board.MIDDLE[0]][Board.MIDDLE[1]] = Letter('A', 1)
        game.board.is_empty = False
        direction = game.is_adjacent((Board.MIDDLE[0], Board.MIDDLE[1]+1))
        self.assertEqual(direction, AdjacentDirection.LEFT)

    def test_is_adjacent_right(self):
        game = Game()
        game.board[Board.MIDDLE[0]][Board.MIDDLE[1]] = Letter('A', 1)
        game.board.is_empty = False
        direction = game.is_adjacent((Board.MIDDLE[0], Board.MIDDLE[1]-1))
        self.assertEqual(direction, AdjacentDirection.RIGHT)

    def test_is_adjacent_below(self):
        game = Game()
        game.board[Board.MIDDLE[0]][Board.MIDDLE[1]] = Letter('A', 1)
        game.board.is_empty = False
        direction = game.is_adjacent((Board.MIDDLE[0]-1, Board.MIDDLE[1]))
        self.assertEqual(direction, AdjacentDirection.BELOW)

    def test_is_adjacent_above(self):
        game = Game()
        game.board[Board.MIDDLE[0]][Board.MIDDLE[1]] = Letter('A', 1)
        game.board.is_empty = False
        direction = game.is_adjacent((Board.MIDDLE[0]+1, Board.MIDDLE[1]))
        self.assertEqual(direction, AdjacentDirection.ABOVE)

    def test_is_adjacent_above_left(self):
        game = Game()
        game.board[Board.MIDDLE[0]][Board.MIDDLE[1]] = Letter('A', 1)
        game.board[Board.MIDDLE[0]+1][Board.MIDDLE[1]] = Letter('B', 1)
        game.board[Board.MIDDLE[0]][Board.MIDDLE[1]+1] = Letter('C', 1)
        game.board.is_empty = False
        direction = game.is_adjacent((Board.MIDDLE[0]+1, Board.MIDDLE[1]+1))
        self.assertEqual(direction,
                         AdjacentDirection.ABOVE | AdjacentDirection.LEFT)

    def test_is_adjacent_above_right(self):
        game = Game()
        game.board[Board.MIDDLE[0]][Board.MIDDLE[1]] = Letter('A', 1)
        game.board[Board.MIDDLE[0]+1][Board.MIDDLE[1]+1] = Letter('B', 1)
        game.board[Board.MIDDLE[0]][Board.MIDDLE[1]+1] = Letter('C', 1)
        game.board.is_empty = False
        direction = game.is_adjacent((Board.MIDDLE[0]+1, Board.MIDDLE[1]))
        self.assertEqual(direction,
                         AdjacentDirection.ABOVE | AdjacentDirection.RIGHT)

    def test_is_adjacent_below_left(self):
        game = Game()
        game.board[Board.MIDDLE[0]][Board.MIDDLE[1]] = Letter('A', 1)
        game.board[Board.MIDDLE[0]-1][Board.MIDDLE[1]] = Letter('B', 1)
        game.board[Board.MIDDLE[0]][Board.MIDDLE[1]+1] = Letter('C', 1)
        game.board.is_empty = False
        direction = game.is_adjacent((Board.MIDDLE[0]-1, Board.MIDDLE[1]+1))
        self.assertEqual(direction,
                         AdjacentDirection.BELOW | AdjacentDirection.LEFT)

    def test_is_adjacent_below_right(self):
        game = Game()
        game.board[Board.MIDDLE[0]][Board.MIDDLE[1]] = Letter('A', 1)
        game.board[Board.MIDDLE[0]-1][Board.MIDDLE[1]+1] = Letter('B', 1)
        game.board[Board.MIDDLE[0]][Board.MIDDLE[1]+1] = Letter('C', 1)
        game.board.is_empty = False
        direction = game.is_adjacent((Board.MIDDLE[0]-1, Board.MIDDLE[1]))
        self.assertEqual(direction,
                         AdjacentDirection.BELOW | AdjacentDirection.RIGHT)

    def test_is_adjacent_left_right(self):
        game = Game()
        game.board[Board.MIDDLE[0]][Board.MIDDLE[1]] = Letter('A', 1)
        game.board[Board.MIDDLE[0]][Board.MIDDLE[1]+2] = Letter('B', 1)
        game.board.is_empty = False
        direction = game.is_adjacent((Board.MIDDLE[0], Board.MIDDLE[1]+1))
        self.assertEqual(direction,
                         AdjacentDirection.LEFT | AdjacentDirection.RIGHT)

    def test_is_adjacent_above_below(self):
        game = Game()
        game.board[Board.MIDDLE[0]][Board.MIDDLE[1]] = Letter('A', 1)
        game.board[Board.MIDDLE[0]+2][Board.MIDDLE[1]] = Letter('B', 1)
        game.board.is_empty = False
        direction = game.is_adjacent((Board.MIDDLE[0]+1, Board.MIDDLE[1]))
        self.assertEqual(direction,
                         AdjacentDirection.ABOVE | AdjacentDirection.BELOW)

    def test_is_adjacent_above_below_left_right(self):
        game = Game()
        game.board[Board.MIDDLE[0]][Board.MIDDLE[1]] = Letter('A', 1)
        game.board[Board.MIDDLE[0]+2][Board.MIDDLE[1]] = Letter('B', 1)
        game.board[Board.MIDDLE[0]+1][Board.MIDDLE[1]+1] = Letter('A', 1)
        game.board[Board.MIDDLE[0]+1][Board.MIDDLE[1]-1] = Letter('B', 1)
        game.board.is_empty = False
        direction = game.is_adjacent((Board.MIDDLE[0]+1, Board.MIDDLE[1]))
        self.assertEqual(direction,
                         AdjacentDirection.LEFT | AdjacentDirection.RIGHT |
                         AdjacentDirection.ABOVE | AdjacentDirection.BELOW)


"""
Commented out until scoring implemented
    # Calculate Score Tests
    def test_calculate_score_simple(self):
        game = Game()
        game.board[Board.MIDDLE[0]][Board.MIDDLE[1]] = Letter('A', 1)
        game.board.is_empty = False
        score = game.calculate_score(
            {(Board.MIDDLE[0], Board.MIDDLE[1]+1): Letter('A', 1)})
        self.assertEqual(score, 2)

    def test_calculate_score_bingo(self):
        game = Game()
        game.board[Board.MIDDLE[0]][Board.MIDDLE[1]] = Letter('A', 1)
        game.board.is_empty = False
        score = game.calculate_score({
            (Board.MIDDLE[0], Board.MIDDLE[1]+1): Letter('A', 1),
            (Board.MIDDLE[0], Board.MIDDLE[1]+2): Letter('A', 1),
            (Board.MIDDLE[0], Board.MIDDLE[1]+3): Letter('A', 1),
            (Board.MIDDLE[0], Board.MIDDLE[1]+4): Letter('A', 1),
            (Board.MIDDLE[0], Board.MIDDLE[1]+5): Letter('A', 1),
            (Board.MIDDLE[0], Board.MIDDLE[1]+6): Letter('A', 1),
            (Board.MIDDLE[0], Board.MIDDLE[1]+7): Letter('A', 1)
            })
        self.assertEqual(score, 58)
"""
