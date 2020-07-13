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
    NOT_ADJACENT = auto()
    NOT_CONTIGUOUS = auto()
    VALID = auto()


class Orientation(Enum):
    NONE = 0
    HORIZONTAL = 1
    VERTICAL = 2


class AdjacentDirection(Flag):
    NONE = 0
    ABOVE = auto()
    BELOW = auto()
    LEFT = auto()
    RIGHT = auto()


class InvalidPlayException(Exception):
    def __init__(self, positions, orientation, valid_reason):
        self.positions = positions
        self.orientation = orientation
        self.valid_reason = valid_reason
        self.message = "{} {} {}".format(positions, orientation, valid_reason)


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
        valid_reason = self.is_valid_play(positions, orientation)
        if valid_reason != ValidationReason.VALID:
            raise InvalidPlayException(positions, orientation, valid_reason)

        # find all words
        words = self.find_words(orientation, letter_positions)

        # calculate score
        score = 0
        for word in words:
            score += self.calculate_score(word)

        # place the letters on the board
        self.board.place_letters(letter_positions)

        return score

    def get_contiguous_cells(self, cell, direction):
        new_word = []
        # return a list of cells that contain letters in direction from cell
        if direction == AdjacentDirection.LEFT:
            row = cell[0]
            col = cell[1] - 1
            while self.board[row][col] is not None and col > 0:
                new_word.insert(0, (row, col))
                col -= 1
        elif direction == AdjacentDirection.RIGHT:
            row = cell[0]
            col = cell[1] + 1
            while self.board[row][col] is not None and col < Board.SIZE:
                new_word.append((row, col))
                col += 1
        elif direction == AdjacentDirection.ABOVE:
            row = cell[0] - 1
            col = cell[1]
            while self.board[row][col] is not None and row > 0:
                new_word.insert(0, (row, col))
                row -= 1
        elif direction == AdjacentDirection.BELOW:
            row = cell[0] + 1
            col = cell[1]
            while self.board[row][col] is not None and row < Board.SIZE:
                new_word.append((row, col))
                row += 1
        return new_word

    def find_words(self, orientation, letter_positions):
        words = set()
        positions = list(letter_positions.keys())

        if len(letter_positions) == 1:
            # handle single-letter play by checking all adjacents
            p = positions[0]
            adjacency = self.is_adjacent(p)

            # find horizontal word
            new_word = [p]
            if adjacency | AdjacentDirection.LEFT:
                new_word.insert(0, self.get_contiguous_cells(positions[0],
                                AdjacentDirection.LEFT))
            if adjacency | AdjacentDirection.RIGHT:
                new_word.insert(-1, self.get_contiguous_cells(positions[0],
                                AdjacentDirection.LEFT))
            # add any word we found
            if len(new_word) > 1:
                words.add(new_word)

            # find vertical word
            new_word = [p]
            if adjacency | AdjacentDirection.ABOVE:
                new_word.insert(0, self.get_contiguous_cells(positions[0],
                                AdjacentDirection.ABOVE))
            if adjacency | AdjacentDirection.BELOW:
                new_word.insert(-1, self.get_contiguous_cells(positions[0],
                                AdjacentDirection.BELOW))
            # add any word we found
            if len(new_word) > 1:
                words.add(new_word)

        elif orientation == Orientation.HORIZONTAL:
            primary_word = positions.copy()
            sorted(primary_word, key=lambda x: x[0])

            # first, add the primary word, extending left and right as needed
            first_adjacents = self.is_adjacent(primary_word[0])
            if first_adjacents | AdjacentDirection.LEFT:
                primary_word.insert(0, self.get_contiguous_cells(
                    positions[0], AdjacentDirection.LEFT))

            last_adjacents = self.is_adjacent(primary_word[-1])
            if last_adjacents | AdjacentDirection.RIGHT:
                primary_word.insert(-1, self.get_contiguous_cells(
                    positions[-1], AdjacentDirection.RIGHT))
            # add the word to our set of words
            words.add(primary_word)

            # next, look for perpendicular words for all letters
            for p in positions:
                adjacency = self.is_adjacent(p)
                new_word = [p]
                if adjacency | AdjacentDirection.ABOVE:
                    new_word.insert(0, self.get_contiguous_cells(p,
                                    AdjacentDirection.ABOVE))
                if adjacency | AdjacentDirection.BELOW:
                    new_word.insert(-1, self.get_contiguous_cells(p,
                                    AdjacentDirection.BELOW))
                # add the word to our set of words
                words.add(new_word)

        elif orientation == Orientation.VERTICAL:
            primary_word = positions.copy()
            sorted(primary_word, key=lambda x: x[1])

            # first, add the primary word, extending above and below as needed
            first_adjacents = self.is_adjacent(primary_word[0])
            if first_adjacents | AdjacentDirection.ABOVE:
                primary_word.insert(0, self.get_contiguous_cells(
                    positions[0], AdjacentDirection.ABOVE))

            last_adjacents = self.is_adjacent(primary_word[-1])
            if last_adjacents | AdjacentDirection.BELOW:
                primary_word.insert(-1, self.get_contiguous_cells(
                    positions[-1], AdjacentDirection.BELOW))
            # add the word to our set of words
            words.add(primary_word)

            # next, look for perpendicular words for all letters
            for p in positions:
                adjacency = self.is_adjacent(p)
                new_word = [p]
                if adjacency | AdjacentDirection.LEFT:
                    new_word.insert(0, self.get_contiguous_cells(
                        p, AdjacentDirection.LEFT))
                if adjacency | AdjacentDirection.RIGHT:
                    new_word.insert(-1, self.get_contiguous_cells(
                        p, AdjacentDirection.RIGHT))
                # add the word to our set of words
                words.add(new_word)

        return words

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
            orientation = Orientation.HORIZONTAL
        elif all(p[1] == col for p in positions):
            orientation = Orientation.VERTICAL

        return orientation

    def is_adjacent(self, position):
        row = position[0]
        col = position[1]
        adjacent_direction = AdjacentDirection.NONE

        # check above, if not at top row
        if row > 0 and self.board[row-1][col] is not None:
            adjacent_direction |= AdjacentDirection.ABOVE
        # check below, if not at bottom row
        if row < Board.SIZE-1 and self.board[row+1][col] is not None:
            adjacent_direction |= AdjacentDirection.BELOW
        # check left, if not at left column
        if col > 0 and self.board[row][col-1] is not None:
            adjacent_direction |= AdjacentDirection.LEFT
        # check right, if not at right column
        if col < Board.SIZE-1 and self.board[row][col+1] is not None:
            adjacent_direction |= AdjacentDirection.RIGHT

        return adjacent_direction

    def is_valid_play(self, positions, orientation):
        # check orientation is either Horizonal or Vertical
        if orientation == Orientation.NONE:
            return ValidationReason.INVALID_ORIENTATION

        # check that first play is on middle cell and
        # is at least 2 letters
        if self.board.is_empty:
            if Board.MIDDLE not in positions:
                return ValidationReason.FIRST_PLAY_NOT_ON_MIDDLE_CELL
            if len(positions) < 2:
                return ValidationReason.FIRST_PLAY_TOO_FEW_TILES
        else:
            # check each cell isn't already full
            if any(self.board[p[0]][p[1]] is not None for p in positions):
                return ValidationReason.CELL_ALREADY_FULL

            # check that play is adjacent to at least one letter
            # previously on the board
            if all(self.is_adjacent(p) == AdjacentDirection.NONE
                   for p in positions):
                return ValidationReason.NOT_ADJACENT

        # check that all played letters are contiguous
        if orientation == Orientation.HORIZONTAL:
            row = positions[0][0]
            for i in range(min(positions, key=lambda x: x[1])[1],
                           max(positions, key=lambda x: x[1])[1]+1):
                if (row, i) not in positions and self.board[row][i] is None:
                    return ValidationReason.NOT_CONTIGUOUS
        elif orientation == Orientation.VERTICAL:
            col = positions[0][1]
            for i in range(min(positions, key=lambda x: x[0])[0],
                           max(positions, key=lambda x: x[0])[0]+1):
                if (i, col) not in positions and self.board[i][col] is None:
                    return ValidationReason.NOT_CONTIGUOUS

        # this is a valid play!
        return ValidationReason.VALID


if __name__ == "__main__":
    pass
