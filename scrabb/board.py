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

        self.double_letter_cells = {
            (3, 0), (11, 0),
            (6, 2), (8, 2),
            (0, 3), (7, 3), (14, 3),
            (2, 6), (6, 6), (8, 6), (12, 6),
            (3, 7), (11, 7),
            (2, 8), (6, 8), (8, 8), (12, 8),
            (0, 11), (7, 11), (14, 11),
            (6, 12), (8, 12),
            (3, 14), (11, 14)
        }

        self.is_empty = True

    def __str__(self):
        printable_board = ""
        for r in range(Board.SIZE):
            for c in range(Board.SIZE):
                if self._board[r][c] is not None:
                    printable_board += "%s " % self._board[r][c].value
                else:
                    printable_board += "0 "
            printable_board += "\n"
        return printable_board

    def __getitem__(self, key):
        return self._board[key]

    def place_letters(self, letter_positions):
        # place letters
        for p in letter_positions:
            self._board[p[0]][p[1]] = letter_positions[p]
        self.is_empty = False