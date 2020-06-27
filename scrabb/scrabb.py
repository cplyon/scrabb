#! /usr/bin/env python3
#
# Scrabble Game
# Author: Chris Lyon
# Contact: chris@cplyon.ca


import math

from collections_extended import bag
from enum import Enum, auto


class ValidationReason(Enum):
    FIRST_PLAY_NOT_ON_MIDDLE_CELL = auto()
    FIRST_PLAY_TOO_FEW_TILES = auto()
    CELL_ALREADY_FULL = auto()
    INVALID_ORIENTATION = auto()
    NOT_TOUCHING_EXISTING = auto()
    NOT_ALL_CONNECTED = auto()
    VALID = auto()


class Orientation(Enum):
    NONE = 0
    HORIZONTAL = 1
    VERTICAL = 2


class NotEnoughLettersException(Exception):
    pass


class Letter:
    def __init__(self, value, score):
        self.value = value
        self.score = score

    def __str__(self):
        print("{0},{1}".format(self.value, self.score))


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

    def play_letters(self, letter_positions):

        # get just the letter positions
        positions = list(letter_positions.keys())

        # determine orientation
        orientation = self.get_orientation(positions)

        # sort positions
        if orientation == Orientation.HORIZONTAL:
            sorted(positions, key=lambda x: x[0])
        elif orientation == Orientation.VERTICAL:
            sorted(positions, key=lambda x: x[1])

        # reject play if not valid
        if self.is_valid_play(positions, orientation) != \
                ValidationReason.VALID:
            return -1
        # place letters
        for p in letter_positions:
            self._board[p[0]][p[1]] = letter_positions[p]
        self.is_empty = False
        # calculate and return score
        score = self.calculate_score(letter_positions)
        return score

    def calculate_score(self, letter_positions):
        # TODO: calculate score for all words found
        # TODO: calculate cell bonuses
        score = 0
        # calculate simple score first
        for p in letter_positions:
            score += letter_positions[p].score

        # bingo bonus
        if len(letter_positions) == 7:
            score += 50
        return score

    def get_orientation(self, positions):
        # Determine word orientation, or NONE if we can't.
        # TODO: how to handle single letter play?
        row = positions[0][0]
        col = positions[0][1]
        orientation = Orientation.NONE

        if all(p[0] == row for p in positions):
            print("Horizontal")
            orientation = Orientation.HORIZONTAL
        elif all(p[1] == col for p in positions):
            print("Vertical")
            orientation = Orientation.VERTICAL

        return orientation

    def is_valid_play(self, positions, orientation):

        # check orientation
        if orientation == Orientation.NONE:
            return ValidationReason.INVALID_ORIENTATION

        # check that first play is on middle cell and is at least
        # 2 letters
        if self.is_empty:
            if Board.MIDDLE not in positions:
                return ValidationReason.FIRST_PLAY_NOT_ON_MIDDLE_CELL
            if len(positions) < 2:
                return ValidationReason.FIRST_PLAY_TOO_FEW_TILES

        # check each cell isn't already full
        if any(self._board[p[0]][p[1]] is not None for p in positions):
            return ValidationReason.CELL_ALREADY_FULL

        # if not first play, check that play touches existing letters
        touching = False
        if not self.is_empty:
            for p in positions:
                # check above, if not at top row
                if p[0] > 0 and self._board[p[0]-1][p[1]] is not None:
                    print("touching above")
                    touching = True
                    break
                # check below, if not at bottom row
                if p[0] < Board.SIZE-1 and \
                        self._board[p[0]+1][p[1]] is not None:
                    print("touching below")
                    touching = True
                    break
                # check left, if not at left column
                if p[1] > 0 and self._board[p[0]][p[1]-1] is not None:
                    print("touching left")
                    touching = True
                    break
                # check right, if not at right column
                if p[1] < Board.SIZE-1 and \
                        self._board[p[0]][p[1]+1] is not None:
                    print("touching right")
                    touching = True
                    break

            # not valid if none touching
            if not touching:
                print("not touching")
                return ValidationReason.NOT_TOUCHING_EXISTING

        # check that all played letters are connected to each other
        # or to previously played letters
        row = positions[0][0]
        col = positions[0][1]
        if orientation == Orientation.HORIZONTAL:
            for i in range(min(positions, key=lambda x: x[1])[1],
                           max(positions, key=lambda x: x[1])[1]+1):
                if (row, i) not in positions and self._board[row][i] is None:
                    return ValidationReason.NOT_ALL_CONNECTED

        if orientation == Orientation.VERTICAL:
            for i in range(min(positions, key=lambda x: x[0])[0],
                           max(positions, key=lambda x: x[0])[0]+1):
                if (i, col) not in positions and self._board[i][col] is None:
                    return ValidationReason.NOT_ALL_CONNECTED

        return ValidationReason.VALID


class Player:

    def __init__(self, name):
        self.name = name
        self.score = 0
        self.letters = bag()


class LetterBag:

    def __init__(self):
        self._letters = bag()

    def __len__(self):
        return len(self._letters)

    def populate_letters(self):
        self._letters.clear()
        self._letters.add(Letter('J', 8))
        self._letters.add(Letter('K', 5))
        self._letters.add(Letter('Q', 10))
        self._letters.add(Letter('X', 8))
        self._letters.add(Letter('Z', 10))
        for _ in range(2):
            self._letters.add(Letter('B', 3))
            self._letters.add(Letter('C', 3))
            self._letters.add(Letter('F', 4))
            self._letters.add(Letter('H', 4))
            self._letters.add(Letter('M', 3))
            self._letters.add(Letter('P', 3))
            self._letters.add(Letter('V', 4))
            self._letters.add(Letter('W', 4))
            self._letters.add(Letter('Y', 4))
            self._letters.add(Letter(' ', 0))
        for _ in range(3):
            self._letters.add(Letter('G', 2))
        for _ in range(4):
            self._letters.add(Letter('D', 2))
            self._letters.add(Letter('L', 1))
            self._letters.add(Letter('S', 1))
            self._letters.add(Letter('U', 1))
        for _ in range(6):
            self._letters.add(Letter('N', 1))
            self._letters.add(Letter('R', 1))
            self._letters.add(Letter('T', 1))
        for _ in range(8):
            self._letters.add(Letter('O', 1))
        for _ in range(9):
            self._letters.add(Letter('A', 1))
            self._letters.add(Letter('I', 1))
        for _ in range(12):
            self._letters.add(Letter('E', 1))

    def draw_letters(self, num_letters):
        # TODO: randomize draw
        drawn_letters = []
        for _ in range(max(num_letters, len(self._letters))):
            drawn_letters.append(self._letters.pop())
        return drawn_letters

    def exchange_letters(self, letters):
        if len(letters) > len(self._letters):
            raise NotEnoughLettersException()

        drawn_letters = self.draw_letters(len(letters))
        for x in letters:
            self._letters.add(x)
        return drawn_letters


class Game:

    def __init__(self):
        self.board = Board()
        self.letter_bag = LetterBag()


if __name__ == "__main__":
    pass
