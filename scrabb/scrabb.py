#! /usr/bin/env python3
#
# Scrabble Game
# Author: Chris Lyon
# Contact: chris@cplyon.ca

from enum import Enum, Flag, auto
from .board import Board
from .tilebag import TileBag


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
        super().__init__()
        self.positions = positions
        self.orientation = orientation
        self.valid_reason = valid_reason
        self.message = f"{positions} {orientation} {valid_reason}"


class Game:

    def __init__(self):
        self.board = Board()
        self.tile_bag = TileBag()
        self.players = []
        self.turn = 0
        self.winner = None

    def play_tiles(self, tile_positions):

        # determine orientation
        orientation = self.get_orientation(tile_positions)

        # sort tiles based on orientation
        if orientation == Orientation.HORIZONTAL:
            tile_positions.sort(key=lambda x: x[1])
        else:
            tile_positions.sort(key=lambda x: x[0])

        # reject play if not valid
        valid_reason = self.is_valid_play(tile_positions, orientation)
        if valid_reason != ValidationReason.VALID:
            raise InvalidPlayException(tile_positions, orientation,
                                       valid_reason)

        # find all words
        words = self.find_words(orientation, tile_positions)

        # calculate score
        score = sum(self.calculate_score(word) for word in words)

        # place the tiles on the board
        self.board.place_tiles(tile_positions)

        return score

    def get_contiguous_cells(self, cell, direction):
        new_word = []
        row = cell[0]
        col = cell[1]

        while True:
            if direction == AdjacentDirection.LEFT:
                col -= 1
            elif direction == AdjacentDirection.RIGHT:
                col += 1
            elif direction == AdjacentDirection.ABOVE:
                row -= 1
            elif direction == AdjacentDirection.BELOW:
                row += 1

            if row < 0 or row >= Board.SIZE or col < 0 or col >= Board.SIZE:
                break

            if self.board[row][col] is None:
                break

            if direction == AdjacentDirection.LEFT or direction == AdjacentDirection.ABOVE:
                new_word.insert(0, (row, col, self.board[row][col]))
            else:
                new_word.append((row, col, self.board[row][col]))

        return new_word

    def extend_word(self, orientation, tile_position):
        adjacency = self.is_adjacent(tile_position)
        cells_front = []
        cells_end = []

        if orientation == Orientation.HORIZONTAL:
            if adjacency | AdjacentDirection.LEFT:
                cells_front = self.get_contiguous_cells(
                    tile_position,
                    AdjacentDirection.LEFT)
            if adjacency | AdjacentDirection.RIGHT:
                cells_end = self.get_contiguous_cells(
                    tile_position,
                    AdjacentDirection.RIGHT)

        elif orientation == Orientation.VERTICAL:
            if adjacency | AdjacentDirection.ABOVE:
                cells_front = self.get_contiguous_cells(
                    tile_position,
                    AdjacentDirection.ABOVE)
            if adjacency | AdjacentDirection.BELOW:
                cells_end = self.get_contiguous_cells(
                    tile_position,
                    AdjacentDirection.BELOW)

        return cells_front + [tile_position] + cells_end

    def find_words(self, orientation, tile_positions):
        # assumes tile_positions are sorted based on orientation

        words = []
        if orientation == Orientation.HORIZONTAL:
            perpendicular_orientation = Orientation.VERTICAL
        else:
            perpendicular_orientation = Orientation.HORIZONTAL

        # first, add the primary word, extending front and end as needed
        front = self.extend_word(orientation, tile_positions[0])
        end = self.extend_word(orientation, tile_positions[-1])
        primary_word = front[0:-1] + tile_positions + end[1:]
        words.append(primary_word)

        # next, look for perpendicular words for all tiles
        for p in tile_positions:
            new_word = self.extend_word(perpendicular_orientation, p)
            # if we find a perpendicular word, add it to our set of words
            if len(new_word) > 1:
                words.append(new_word)

        return words

    def calculate_score(self, tile_positions):
        score = 0
        word_multiplier = 1

        # calculate tile scores
        current_score = 0
        for p in tile_positions:
            # calculate word bonuses
            if (p[0], p[1]) in self.board.double_word_cells:
                word_multiplier *= 2
            elif (p[0], p[1]) in self.board.triple_word_cells:
                word_multiplier *= 3
            # calculate letter bonuses
            if (p[0], p[1]) in self.board.double_letter_cells:
                current_score += (p[2].score * 2)
            elif (p[0], p[1]) in self.board.triple_letter_cells:
                current_score += (p[2].score * 3)
            else:
                current_score += p[2].score
        score = current_score * word_multiplier

        # bingo bonus
        if len(tile_positions) == 7:
            score += 50
        return score

    def get_orientation(self, positions):
        # Determine word orientation, or NONE if we can't.
        # Treat single tile plays as Horizontal
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

    def is_valid_play(self, tile_positions, orientation):
        # check orientation is either Horizonal or Vertical
        if orientation == Orientation.NONE:
            return ValidationReason.INVALID_ORIENTATION

        # get just the tile positions, since we don't need the actual tile
        # to determine if the play is valid
        positions = [(p[0], p[1]) for p in tile_positions]

        # check that first play is on middle cell and
        # is at least 2 tiles
        if self.board.is_empty:
            if Board.MIDDLE not in positions:
                return ValidationReason.FIRST_PLAY_NOT_ON_MIDDLE_CELL
            if len(positions) < 2:
                return ValidationReason.FIRST_PLAY_TOO_FEW_TILES
        else:
            # check each cell isn't already full
            if any(self.board[p[0]][p[1]] is not None
                   for p in positions):
                return ValidationReason.CELL_ALREADY_FULL

            # check that play is adjacent to at least one tile
            # already on the board
            if all(self.is_adjacent(p) == AdjacentDirection.NONE
                   for p in positions):
                return ValidationReason.NOT_ADJACENT

        # check that all played tiles are contiguous
        if orientation == Orientation.HORIZONTAL:
            row = positions[0][0]
            if any((row, i) not in positions and self.board[row][i] is None
                   for i in range(positions[0][1],
                                  max(positions, key=lambda x: x[1])[1]+1)):
                return ValidationReason.NOT_CONTIGUOUS
        elif orientation == Orientation.VERTICAL:
            col = positions[0][1]
            if any((i, col) not in positions and self.board[i][col] is None
                   for i in range(positions[0][0],
                                  max(positions, key=lambda x: x[0])[0]+1)):
                return ValidationReason.NOT_CONTIGUOUS

        # this is a valid play!
        return ValidationReason.VALID


if __name__ == "__main__":
    pass
