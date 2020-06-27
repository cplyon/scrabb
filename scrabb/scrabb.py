#! /usr/bin/env python3
#
# Scrabble Game
# Author: Chris Lyon
# Contact: chris@cplyon.ca

from .board import Board
from .letterbag import LetterBag
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


class Game:

    def __init__(self):
        self.board = Board()
        self.letter_bag = LetterBag()

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
        if self.board.is_empty:
            if Board.MIDDLE not in positions:
                return ValidationReason.FIRST_PLAY_NOT_ON_MIDDLE_CELL
            if len(positions) < 2:
                return ValidationReason.FIRST_PLAY_TOO_FEW_TILES

        # check each cell isn't already full
        if any(self.board[p[0]][p[1]] is not None for p in positions):
            return ValidationReason.CELL_ALREADY_FULL

        # if not first play, check that play touches existing letters
        touching = False
        if not self.board.is_empty:
            for p in positions:
                # check above, if not at top row
                if p[0] > 0 and self.board[p[0]-1][p[1]] is not None:
                    print("touching above")
                    touching = True
                    break
                # check below, if not at bottom row
                if p[0] < Board.SIZE-1 and \
                        self.board[p[0]+1][p[1]] is not None:
                    print("touching below")
                    touching = True
                    break
                # check left, if not at left column
                if p[1] > 0 and self.board[p[0]][p[1]-1] is not None:
                    print("touching left")
                    touching = True
                    break
                # check right, if not at right column
                if p[1] < Board.SIZE-1 and \
                        self.board[p[0]][p[1]+1] is not None:
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
                if (row, i) not in positions and self.board[row][i] is None:
                    return ValidationReason.NOT_ALL_CONNECTED

        if orientation == Orientation.VERTICAL:
            for i in range(min(positions, key=lambda x: x[0])[0],
                           max(positions, key=lambda x: x[0])[0]+1):
                if (i, col) not in positions and self.board[i][col] is None:
                    return ValidationReason.NOT_ALL_CONNECTED

        return ValidationReason.VALID


if __name__ == "__main__":
    pass
