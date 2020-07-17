#!/usr/bin/env python3
#
# Scrabble Game Tests
# Author: Chris Lyon
# Contact: chris@cplyon.ca

import unittest

from scrabb.board import Board
from scrabb.tile import Tile
from scrabb.scrabb import Game
from scrabb.scrabb import InvalidPlayException
from scrabb.scrabb import Orientation
from scrabb.scrabb import AdjacentDirection
from scrabb.scrabb import ValidationReason


class GameTest(unittest.TestCase):

    A = Tile('A', 1)
    B = Tile('B', 1)
    C = Tile('C', 1)
    L = Tile('L', 1)
    R = Tile('R', 1)

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
        game.board[Board.MIDDLE[0]][Board.MIDDLE[1]] = self.A
        is_valid = game.is_valid_play([Board.MIDDLE], Orientation.HORIZONTAL)
        self.assertEqual(is_valid,
                         ValidationReason.FIRST_PLAY_TOO_FEW_TILES)

    def test_is_valid_cell_full(self):
        game = Game()
        game.board[Board.MIDDLE[0]][Board.MIDDLE[1]] = self.A
        game.board.is_empty = False
        is_valid = game.is_valid_play([Board.MIDDLE], Orientation.HORIZONTAL)
        self.assertEqual(is_valid,
                         ValidationReason.CELL_ALREADY_FULL)

    def test_is_valid_not_adjacent(self):
        game = Game()
        game.board[Board.MIDDLE[0]][Board.MIDDLE[1]] = self.A
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
        game.board[Board.MIDDLE[0]][Board.MIDDLE[1]] = self.A
        game.board.is_empty = False
        is_valid = game.is_valid_play([(Board.MIDDLE[0], Board.MIDDLE[1]-1),
                                       (Board.MIDDLE[0], Board.MIDDLE[1]+1)],
                                      Orientation.HORIZONTAL)
        self.assertEqual(is_valid, ValidationReason.VALID)

    def test_is_valid_prefix_suffix_vertical(self):
        game = Game()
        game.board[Board.MIDDLE[0]][Board.MIDDLE[1]] = self.A
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

    # Play Tiles Tests
    def test_play_tiles_invalid(self):
        position = (Board.MIDDLE[0], Board.MIDDLE[1]+4)
        game = Game()
        with self.assertRaises(InvalidPlayException) as e:
            game.play_tiles(
                [(position[0], position[1], self.A)])
            self.assertEqual(e.positions, [position])
            self.assertEqual(e.orientation, Orientation.HORIZONTAL)
            self.assertEqual(e.valid_reason,
                             ValidationReason.FIRST_PLAY_TOO_FEW_TILES)

    def test_play_files_valid(self):
        game = Game()
        score = game.play_tiles([
            (Board.MIDDLE[0], Board.MIDDLE[1], self.A),
            (Board.MIDDLE[0], Board.MIDDLE[1]+1, self.B)
        ])
        self.assertEqual(score, 4)

    # Is Adjacent Tests
    def test_is_adjacent_none(self):
        game = Game()
        game.board[Board.MIDDLE[0]][Board.MIDDLE[1]] = self.A
        direction = game.is_adjacent((Board.MIDDLE[0], Board.MIDDLE[1]+4))
        self.assertEqual(direction, AdjacentDirection.NONE)

    def test_is_adjacent_left(self):
        game = Game()
        game.board[Board.MIDDLE[0]][Board.MIDDLE[1]] = self.A
        direction = game.is_adjacent((Board.MIDDLE[0], Board.MIDDLE[1]+1))
        self.assertEqual(direction, AdjacentDirection.LEFT)

    def test_is_adjacent_right(self):
        game = Game()
        game.board[Board.MIDDLE[0]][Board.MIDDLE[1]] = self.A
        direction = game.is_adjacent((Board.MIDDLE[0], Board.MIDDLE[1]-1))
        self.assertEqual(direction, AdjacentDirection.RIGHT)

    def test_is_adjacent_below(self):
        game = Game()
        game.board[Board.MIDDLE[0]][Board.MIDDLE[1]] = self.A
        direction = game.is_adjacent((Board.MIDDLE[0]-1, Board.MIDDLE[1]))
        self.assertEqual(direction, AdjacentDirection.BELOW)

    def test_is_adjacent_above(self):
        game = Game()
        game.board[Board.MIDDLE[0]][Board.MIDDLE[1]] = self.A
        direction = game.is_adjacent((Board.MIDDLE[0]+1, Board.MIDDLE[1]))
        self.assertEqual(direction, AdjacentDirection.ABOVE)

    def test_is_adjacent_above_left(self):
        game = Game()
        game.board[Board.MIDDLE[0]][Board.MIDDLE[1]] = self.A
        game.board[Board.MIDDLE[0]+1][Board.MIDDLE[1]] = self.B
        game.board[Board.MIDDLE[0]][Board.MIDDLE[1]+1] = self.C
        direction = game.is_adjacent((Board.MIDDLE[0]+1, Board.MIDDLE[1]+1))
        self.assertEqual(direction,
                         AdjacentDirection.ABOVE | AdjacentDirection.LEFT)

    def test_is_adjacent_above_right(self):
        game = Game()
        game.board[Board.MIDDLE[0]][Board.MIDDLE[1]] = self.A
        game.board[Board.MIDDLE[0]+1][Board.MIDDLE[1]+1] = self.B
        game.board[Board.MIDDLE[0]][Board.MIDDLE[1]+1] = self.C
        direction = game.is_adjacent((Board.MIDDLE[0]+1, Board.MIDDLE[1]))
        self.assertEqual(direction,
                         AdjacentDirection.ABOVE | AdjacentDirection.RIGHT)

    def test_is_adjacent_below_left(self):
        game = Game()
        game.board[Board.MIDDLE[0]][Board.MIDDLE[1]] = self.A
        game.board[Board.MIDDLE[0]-1][Board.MIDDLE[1]] = self.B
        game.board[Board.MIDDLE[0]][Board.MIDDLE[1]+1] = self.C
        direction = game.is_adjacent((Board.MIDDLE[0]-1, Board.MIDDLE[1]+1))
        self.assertEqual(direction,
                         AdjacentDirection.BELOW | AdjacentDirection.LEFT)

    def test_is_adjacent_below_right(self):
        game = Game()
        game.board[Board.MIDDLE[0]][Board.MIDDLE[1]] = self.A
        game.board[Board.MIDDLE[0]-1][Board.MIDDLE[1]+1] = self.B
        game.board[Board.MIDDLE[0]][Board.MIDDLE[1]+1] = self.C
        direction = game.is_adjacent((Board.MIDDLE[0]-1, Board.MIDDLE[1]))
        self.assertEqual(direction,
                         AdjacentDirection.BELOW | AdjacentDirection.RIGHT)

    def test_is_adjacent_left_right(self):
        game = Game()
        game.board[Board.MIDDLE[0]][Board.MIDDLE[1]] = self.A
        game.board[Board.MIDDLE[0]][Board.MIDDLE[1]+2] = self.B
        direction = game.is_adjacent((Board.MIDDLE[0], Board.MIDDLE[1]+1))
        self.assertEqual(direction,
                         AdjacentDirection.LEFT | AdjacentDirection.RIGHT)

    def test_is_adjacent_above_below(self):
        game = Game()
        game.board[Board.MIDDLE[0]][Board.MIDDLE[1]] = self.A
        game.board[Board.MIDDLE[0]+2][Board.MIDDLE[1]] = self.B
        direction = game.is_adjacent((Board.MIDDLE[0]+1, Board.MIDDLE[1]))
        self.assertEqual(direction,
                         AdjacentDirection.ABOVE | AdjacentDirection.BELOW)

    def test_is_adjacent_above_below_left_right(self):
        game = Game()
        game.board[Board.MIDDLE[0]][Board.MIDDLE[1]] = self.A
        game.board[Board.MIDDLE[0]+2][Board.MIDDLE[1]] = self.B
        game.board[Board.MIDDLE[0]+1][Board.MIDDLE[1]+1] = self.A
        game.board[Board.MIDDLE[0]+1][Board.MIDDLE[1]-1] = self.B
        direction = game.is_adjacent((Board.MIDDLE[0]+1, Board.MIDDLE[1]))
        self.assertEqual(direction,
                         AdjacentDirection.LEFT | AdjacentDirection.RIGHT |
                         AdjacentDirection.ABOVE | AdjacentDirection.BELOW)

    # Get Contiguous tests
    def test_get_contiguous_left(self):
        game = Game()
        game.board[Board.MIDDLE[0]][Board.MIDDLE[1]-1] = self.L
        game.board[Board.MIDDLE[0]][Board.MIDDLE[1]-2] = self.L
        game.board[Board.MIDDLE[0]][Board.MIDDLE[1]-3] = self.L
        game.board[Board.MIDDLE[0]][Board.MIDDLE[1]-5] = self.L
        word = game.get_contiguous_cells(Board.MIDDLE, AdjacentDirection.LEFT)
        self.assertListEqual(word, [(Board.MIDDLE[0], Board.MIDDLE[1]-3, self.L),
                                    (Board.MIDDLE[0], Board.MIDDLE[1]-2, self.L),
                                    (Board.MIDDLE[0], Board.MIDDLE[1]-1, self.L)
                                    ])

    def test_get_contiguous_right(self):
        game = Game()
        game.board[Board.MIDDLE[0]][Board.MIDDLE[1]+1] = self.R
        game.board[Board.MIDDLE[0]][Board.MIDDLE[1]+2] = self.R
        game.board[Board.MIDDLE[0]][Board.MIDDLE[1]+3] = self.R
        game.board[Board.MIDDLE[0]][Board.MIDDLE[1]+5] = self.R
        word = game.get_contiguous_cells(Board.MIDDLE, AdjacentDirection.RIGHT)
        self.assertListEqual(word, [(Board.MIDDLE[0], Board.MIDDLE[1]+1, self.R),
                                    (Board.MIDDLE[0], Board.MIDDLE[1]+2, self.R),
                                    (Board.MIDDLE[0], Board.MIDDLE[1]+3, self.R)
                                    ])

    def test_get_contiguous_above(self):
        game = Game()
        game.board[Board.MIDDLE[0]-1][Board.MIDDLE[1]] = self.A
        game.board[Board.MIDDLE[0]-2][Board.MIDDLE[1]] = self.A
        game.board[Board.MIDDLE[0]-3][Board.MIDDLE[1]] = self.A
        game.board[Board.MIDDLE[0]-5][Board.MIDDLE[1]] = self.A
        word = game.get_contiguous_cells(Board.MIDDLE, AdjacentDirection.ABOVE)
        self.assertListEqual(word, [(Board.MIDDLE[0]-3, Board.MIDDLE[1], self.A),
                                    (Board.MIDDLE[0]-2, Board.MIDDLE[1], self.A),
                                    (Board.MIDDLE[0]-1, Board.MIDDLE[1], self.A)
                                    ])

    def test_get_contiguous_below(self):
        game = Game()
        game.board[Board.MIDDLE[0]+1][Board.MIDDLE[1]] = self.B
        game.board[Board.MIDDLE[0]+2][Board.MIDDLE[1]] = self.B
        game.board[Board.MIDDLE[0]+3][Board.MIDDLE[1]] = self.B
        game.board[Board.MIDDLE[0]+5][Board.MIDDLE[1]] = self.B
        word = game.get_contiguous_cells(Board.MIDDLE, AdjacentDirection.BELOW)
        self.assertListEqual(word, [(Board.MIDDLE[0]+1, Board.MIDDLE[1], self.B),
                                    (Board.MIDDLE[0]+2, Board.MIDDLE[1], self.B),
                                    (Board.MIDDLE[0]+3, Board.MIDDLE[1], self.B)
                                    ])

    def test_get_contiguous_none(self):
        game = Game()
        word = game.get_contiguous_cells(Board.MIDDLE, AdjacentDirection.LEFT)
        self.assertListEqual(word, [])

    # Find Words tests
    def test_find_words_none(self):
        game = Game()
        words = game.find_words(Orientation.HORIZONTAL,
                                [(Board.MIDDLE[0], Board.MIDDLE[1],
                                 self.A)])
        self.assertEqual(words, [])

    def test_find_words_extend_left(self):
        game = Game()
        game.board[Board.MIDDLE[0]][Board.MIDDLE[1]+1] = self.R
        game.board[Board.MIDDLE[0]][Board.MIDDLE[1]+2] = self.R
        game.board[Board.MIDDLE[0]][Board.MIDDLE[1]+3] = self.R
        game.board.is_empty = False
        words = game.find_words(Orientation.HORIZONTAL,
                                [(Board.MIDDLE[0], Board.MIDDLE[1],
                                 self.A),
                                 (Board.MIDDLE[0], Board.MIDDLE[1]-1,
                                 self.A)])
        self.assertListEqual(words, [[
            (Board.MIDDLE[0], Board.MIDDLE[1]-1, self.A),
            (Board.MIDDLE[0], Board.MIDDLE[1], self.A),
            (Board.MIDDLE[0], Board.MIDDLE[1]+1, self.R),
            (Board.MIDDLE[0], Board.MIDDLE[1]+2, self.R),
            (Board.MIDDLE[0], Board.MIDDLE[1]+3, self.R)
        ]])

    def test_find_words_extend_right(self):
        game = Game()
        game.board[Board.MIDDLE[0]][Board.MIDDLE[1]-1] = self.L
        game.board[Board.MIDDLE[0]][Board.MIDDLE[1]-2] = self.L
        game.board[Board.MIDDLE[0]][Board.MIDDLE[1]-3] = self.L
        game.board.is_empty = False
        words = game.find_words(Orientation.HORIZONTAL,
                                [(Board.MIDDLE[0], Board.MIDDLE[0],
                                 self.A),
                                 (Board.MIDDLE[0], Board.MIDDLE[0]+1,
                                 self.A)])
        self.assertListEqual(words, [[
            (Board.MIDDLE[0], Board.MIDDLE[1]-3, self.L),
            (Board.MIDDLE[0], Board.MIDDLE[1]-2, self.L),
            (Board.MIDDLE[0], Board.MIDDLE[1]-1, self.L),
            (Board.MIDDLE[0], Board.MIDDLE[1], self.A),
            (Board.MIDDLE[0], Board.MIDDLE[1]+1, self.A)
        ]])

    def test_find_words_extend_above(self):
        game = Game()
        game.board[Board.MIDDLE[0]+1][Board.MIDDLE[1]] = self.B
        game.board[Board.MIDDLE[0]+2][Board.MIDDLE[1]] = self.B
        game.board[Board.MIDDLE[0]+3][Board.MIDDLE[1]] = self.B
        game.board.is_empty = False
        words = game.find_words(Orientation.VERTICAL,
                                [(Board.MIDDLE[0], Board.MIDDLE[1],
                                 self.A),
                                 (Board.MIDDLE[0]-1, Board.MIDDLE[1],
                                 self.A)
                                 ])
        self.assertListEqual(words, [[
            (Board.MIDDLE[0]-1, Board.MIDDLE[1], self.A),
            (Board.MIDDLE[0], Board.MIDDLE[1], self.A),
            (Board.MIDDLE[0]+1, Board.MIDDLE[1], self.B),
            (Board.MIDDLE[0]+2, Board.MIDDLE[1], self.B),
            (Board.MIDDLE[0]+3, Board.MIDDLE[1], self.B)
        ]])

    def test_find_words_extend_below(self):
        game = Game()
        game.board[Board.MIDDLE[0]-1][Board.MIDDLE[1]] = self.A
        game.board[Board.MIDDLE[0]-2][Board.MIDDLE[1]] = self.A
        game.board[Board.MIDDLE[0]-3][Board.MIDDLE[1]] = self.A
        game.board.is_empty = False
        words = game.find_words(Orientation.VERTICAL,
                                [(Board.MIDDLE[0], Board.MIDDLE[1],
                                 self.A),
                                 (Board.MIDDLE[1]+1, Board.MIDDLE[1],
                                 self.A)
                                 ])
        self.assertListEqual(words, [[
            (Board.MIDDLE[0]-3, Board.MIDDLE[1], self.A),
            (Board.MIDDLE[0]-2, Board.MIDDLE[1], self.A),
            (Board.MIDDLE[0]-1, Board.MIDDLE[1], self.A),
            (Board.MIDDLE[0], Board.MIDDLE[1], self.A),
            (Board.MIDDLE[0]+1, Board.MIDDLE[1], self.A)
        ]])

    def test_find_words_horizontal_parallel(self):
        game = Game()
        game.board[Board.MIDDLE[0]][Board.MIDDLE[1]] = self.R
        game.board[Board.MIDDLE[0]][Board.MIDDLE[1]+1] = self.R
        game.board[Board.MIDDLE[0]][Board.MIDDLE[1]+2] = self.R
        game.board.is_empty = False
        words = game.find_words(Orientation.HORIZONTAL,
                                [(Board.MIDDLE[0]+1, Board.MIDDLE[1],
                                 self.A),
                                 (Board.MIDDLE[0]+1, Board.MIDDLE[1]+1,
                                 self.A)])
        self.assertListEqual(words, [
            [(Board.MIDDLE[0]+1, Board.MIDDLE[1], self.A),
             (Board.MIDDLE[0]+1, Board.MIDDLE[1]+1, self.A)],
            [(Board.MIDDLE[0], Board.MIDDLE[1], self.R),
             (Board.MIDDLE[0]+1, Board.MIDDLE[1], self.A)],
            [(Board.MIDDLE[0], Board.MIDDLE[1]+1, self.R),
             (Board.MIDDLE[0]+1, Board.MIDDLE[1]+1, self.A)]
        ])

    def test_find_words_vertical_parallel(self):
        game = Game()
        game.board[Board.MIDDLE[0]][Board.MIDDLE[1]] = self.B
        game.board[Board.MIDDLE[0]+1][Board.MIDDLE[1]] = self.B
        game.board.is_empty = False
        words = game.find_words(Orientation.VERTICAL,
                                [(Board.MIDDLE[0], Board.MIDDLE[1]+1,
                                 self.A),
                                 (Board.MIDDLE[0]+1, Board.MIDDLE[1]+1,
                                 self.A)])
        self.assertListEqual(words, [
            [(Board.MIDDLE[0], Board.MIDDLE[1]+1, self.A),
             (Board.MIDDLE[0]+1, Board.MIDDLE[1]+1, self.A)],
            [(Board.MIDDLE[0], Board.MIDDLE[1], self.B),
             (Board.MIDDLE[0], Board.MIDDLE[1]+1, self.A)],
            [(Board.MIDDLE[0]+1, Board.MIDDLE[1], self.B),
             (Board.MIDDLE[0]+1, Board.MIDDLE[1]+1, self.A)]
        ])

    # Calculate Score Tests
    def test_calculate_score_simple(self):
        game = Game()
        game.board[Board.MIDDLE[0]][Board.MIDDLE[1]] = self.A
        score = game.calculate_score(
            [(Board.MIDDLE[0], Board.MIDDLE[1]+1, self.A)])
        self.assertEqual(score, 1)

    def test_calculate_score_double_word(self):
        game = Game()
        score = game.calculate_score([
            (Board.MIDDLE[0], Board.MIDDLE[1], self.A),
            (Board.MIDDLE[0], Board.MIDDLE[1]+1, self.A),
        ])
        self.assertEqual(score, 4)

    def test_calculate_score_triple_word(self):
        game = Game()
        score = game.calculate_score([
            (0, Board.MIDDLE[1], self.A),
            (0, Board.MIDDLE[1]+1, self.A),
        ])
        self.assertEqual(score, 6)

    def test_calculate_score_double_letter(self):
        game = Game()
        score = game.calculate_score([
            (Board.MIDDLE[0]-1, Board.MIDDLE[1], self.A),
            (Board.MIDDLE[0]-1, Board.MIDDLE[1]+1, self.A),
        ])
        self.assertEqual(score, 3)

    def test_calculate_score_triple_letter(self):
        game = Game()
        score = game.calculate_score([
            (Board.MIDDLE[0]-2, Board.MIDDLE[1]+1, self.A),
            (Board.MIDDLE[0]-2, Board.MIDDLE[1]+2, self.A),
        ])
        self.assertEqual(score, 4)

    def test_calculate_score_bingo(self):
        game = Game()
        game.board[Board.MIDDLE[0]][Board.MIDDLE[1]] = self.A
        score = game.calculate_score([
            (Board.MIDDLE[0]+1, Board.MIDDLE[1], self.A),
            (Board.MIDDLE[0]+1, Board.MIDDLE[1]+1, self.A),
            (Board.MIDDLE[0]+1, Board.MIDDLE[1]+2, self.A),
            (Board.MIDDLE[0]+1, Board.MIDDLE[1]+3, self.A),
            (Board.MIDDLE[0]+1, Board.MIDDLE[1]+4, self.A),
            (Board.MIDDLE[0]+1, Board.MIDDLE[1]+5, self.A),
            (Board.MIDDLE[0]+1, Board.MIDDLE[1]+6, self.A)
        ])
        self.assertEqual(score, 59)
