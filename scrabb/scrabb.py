#! /usr/bin/env python3
#
# Scrabble Game
# Author: Chris Lyon
# Contact: chris@cplyon.ca

from .board import Board
from .letterbag import LetterBag
from enum import Enum, Flag, auto


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


class TouchingDirection(Flag):
    NONE = 0
    ABOVE = auto()
    BELOW = auto()
    LEFT = auto()
    RIGHT = auto()


class Game:

    def __init__(self):
        self.board = Board()
        self.letter_bag = LetterBag()

    def play_letters(self, letter_positions):

        # get just the letter positions
        positions = list(letter_positions.keys())

        # determine orientation
        orientation = self.get_orientation(positions)

        # reject play if not valid
        if self.is_valid_play(positions, orientation) != \
                ValidationReason.VALID:
            return -1

        # find all words
        words = self.find_words(orientation, letter_positions)

        # calculate score
        score = 0
        for word in words:
            score += self.calculate_score(positions, letter_positions)

        # place the letters on the board
        self.board.place_letters(letter_positions)

        return score

    def find_words(self, orientation, letter_positions):
        # sort positions
        positions = list(letter_positions.keys())
        if orientation == Orientation.HORIZONTAL:
            sorted(positions, key=lambda x: x[0])
        elif orientation == Orientation.VERTICAL:
            sorted(positions, key=lambda x: x[1])

        # find all words and store in a collection of tuples or dicts?
        # if horizontal:
        # first, calculate main word
        # include the non-empty cells to the left of the first letter
        # include the non-empty cells to the right of the last letter
        # add this word to collection
        # now find adjacent words
        # for each letter played, if above cell is not empty:
        # include all non-empty cells above the current letter
        # include all non-empty cells below the current letter
        # add this word to collection
        # number of words is between 1 and (1 + len(positions))
        # modify and repeat for vertical play
        return None

    def calculate_score(self, letter_positions):
        score = 0

        # calculate letter scores
        for p in letter_positions:
            # TODO: calculate cell bonuses
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

    def is_touching(self, position):
        touching_direction = TouchingDirection.NONE
        # check above, if not at top row
        if position[0] > 0 and \
                self.board[position[0]+1][position[1]] is not None:
            print("touching above")
            touching_direction |= TouchingDirection.ABOVE
        # check below, if not at bottom row
        if position[0] < Board.SIZE-1 and \
                self.board[position[0]-1][position[1]] is not None:
            print("touching below")
            touching_direction |= TouchingDirection.BELOW
        # check left, if not at left column
        if position[1] > 0 and \
                self.board[position[0]][position[1]-1] is not None:
            print("touching left")
            touching_direction |= TouchingDirection.LEFT
        # check right, if not at right column
        if position[1] < Board.SIZE-1 and \
                self.board[position[0]][position[1]+1] is not None:
            print("touching right")
            touching_direction |= TouchingDirection.RIGHT

        return touching_direction

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
        else:
            # check each cell isn't already full
            if any(self.board[p[0]][p[1]] is not None for p in positions):
                return ValidationReason.CELL_ALREADY_FULL

            # check that play touches existing letters
            for p in positions:
                if self.is_touching(p) != TouchingDirection.NONE:
                    break
            else:
                # not valid if none touching
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
