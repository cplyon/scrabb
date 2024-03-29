#! /usr/bin/env python3
#
# Scrabble Game
# Author: Chris Lyon
# Contact: chris@cplyon.ca

import math


class Board:
    SIZE = 15
    MIDDLE = (math.floor(SIZE/2), math.floor(SIZE/2))

    def __init__(self):
        self._board = [[None for _ in range(Board.SIZE)]
                       for _ in range(Board.SIZE)]
        self.is_empty = True

        self.double_letter_cells = {
            (0, 3), (0, 11),
            (2, 6), (2, 8),
            (3, 0), (3, 7), (3, 14),
            (6, 2), (6, 6), (6, 8), (6, 12),
            (7, 3), (7, 11),
            (8, 2), (8, 6), (8, 8), (8, 12),
            (11, 0), (11, 7), (11, 14),
            (12, 6), (12, 8),
            (14, 3), (14, 11)
        }

        self.triple_letter_cells = {
            (1, 5), (1, 9),
            (5, 1), (5, 5), (5, 9), (5, 13),
            (9, 1), (9, 5), (9, 9), (9, 13),
            (13, 5), (13, 9)
        }

        self.double_word_cells = {
            (1, 1), (1, 13),
            (2, 3), (2, 12),
            (3, 3), (3, 11),
            (4, 4), (4, 10),
            (7, 7),
            (10, 4), (10, 10),
            (11, 3), (11, 11),
            (12, 2), (12, 12),
            (13, 1), (13, 13)
        }
        self.triple_word_cells = {
            (0, 0), (0, 7), (0, 14),
            (7, 0), (7, 14),
            (14, 0), (14, 7), (14, 14)
        }

    def __str__(self):
        printable_board = ""
        for row in range(Board.SIZE):
            for col in range(Board.SIZE):
                if self._board[row][col] is not None:
                    printable_board += f"{self._board[row][col].value} "
                else:
                    printable_board += "0 "
            printable_board += "\n"
        return printable_board

    def __getitem__(self, key):
        return self._board[key]

    def place_tiles(self, tile_positions):
        for pos in tile_positions:
            position = (pos[0], pos[1])
            # remove any square bonuses
            self.double_letter_cells.discard(position)
            self.triple_letter_cells.discard(position)
            self.double_word_cells.discard(position)
            self.triple_word_cells.discard(position)
            # place tile
            self._board[pos[0]][pos[1]] = pos[2]
        self.is_empty = False
