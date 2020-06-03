#! /usr/bin/env python3
#
# Scrabble Game
# Author: Chris Lyon
# Contact: chris@cplyon.ca


import math

from collections_extended import bag
from enum import Enum


class Orientation(Enum):
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
        score = 0
        if not self.is_valid_play(list(letter_positions.keys())):
            return -1
        for p in letter_positions:
            self._board[p[0]][p[1]] = letter_positions[p]
            score += letter_positions[p].score
            self.is_empty = False

        # TODO: need to calculate full score based on existing letters
        return score

    def remove_letters(self, positions):
        pass

    def is_valid_play(self, positions):
        row = -1
        col = -1
        orientation = None
        touching = False

        # check that first play is on middle cell
        if self.is_empty:
            if Board.MIDDLE not in positions:
                return False

        for p in positions:
            # check that cell isn't already full
            if self._board[p[0]][p[1]] is not None:
                return False

            # check that all letters are in the same col or row and
            # determine word orientation
            if orientation is None:
                if row == -1 or col == -1:
                    row = positions[0][0]
                    col = positions[0][1]
                elif p[0] == row:
                    print("Horizontal")
                    orientation = Orientation.HORIZONTAL
                elif p[1] == col:
                    print("Vertical")
                    orientation = Orientation.VERTICAL
                else:
                    return False
            elif orientation == Orientation.HORIZONTAL and p[0] != row:
                return False
            elif orientation == Orientation.VERTICAL and p[1] != col:
                return False

            # if not first play, check that play touches existing letters
            if not self.is_empty and not touching:
                print("checking touch")
                # check above, if not at top row
                if ((p[0]-1, p[1]) not in positions) and \
                        (p[0] > 0 and
                            self._board[p[0]-1][p[1]] is not None):
                    print("touching above")
                    touching = True
                # check below, if not at bottom row
                if ((p[0]+1, p[1]) not in positions) and \
                        (p[0] < Board.SIZE-1 and
                            self._board[p[0]+1][p[1]] is not None):
                    print("touching below")
                    touching = True
                # check left, if not at left column
                if ((p[0], p[1]-1) not in positions) and \
                        (p[1] > 0 and
                            self._board[p[0]][p[1]-1] is not None):
                    print("touching left")
                    touching = True
                # check right, if not at right column
                if ((p[0], p[1]+1) not in positions) and \
                        (p[1] < Board.SIZE-1 and
                            self._board[p[0]][p[1]+1] is not None):
                    print("touching right")
                    touching = True

        # check at least one letter touches existing, unless first play
        if not self.is_empty and not touching:
            print("not touching", p)
            return False

        # check that all played letters are connected
        if orientation == Orientation.HORIZONTAL:
            print("H check", positions)
            for i in range(min(positions, key=lambda x: x[1])[1],
                           max(positions, key=lambda x: x[1])[1]+1):
                if (positions[0][0], i) not in positions:
                    print("H check false")
                    return False
        elif orientation == Orientation.VERTICAL:
            print("V check", positions)
            for i in range(min(positions, key=lambda x: x[0])[0],
                           max(positions, key=lambda x: x[0])[0]+1):
                if (i, positions[0][0]) not in positions:
                    print("V check false")
                    return False

        return True


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
