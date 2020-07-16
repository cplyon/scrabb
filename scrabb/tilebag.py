#! /usr/bin/env python3
#
# Scrabble Game
# Author: Chris Lyon
# Contact: chris@cplyon.ca

from .tile import Tile
from collections_extended import bag


class NotEnoughTilesException(Exception):
    pass


class TileBag:

    def __init__(self):
        self._tiles = bag()

    def __len__(self):
        return len(self._tiles)

    def populate_tiles(self):
        self._tiles.clear()
        self._tiles.add(Tile('J', 8))
        self._tiles.add(Tile('K', 5))
        self._tiles.add(Tile('Q', 10))
        self._tiles.add(Tile('X', 8))
        self._tiles.add(Tile('Z', 10))
        for _ in range(2):
            self._tiles.add(Tile('B', 3))
            self._tiles.add(Tile('C', 3))
            self._tiles.add(Tile('F', 4))
            self._tiles.add(Tile('H', 4))
            self._tiles.add(Tile('M', 3))
            self._tiles.add(Tile('P', 3))
            self._tiles.add(Tile('V', 4))
            self._tiles.add(Tile('W', 4))
            self._tiles.add(Tile('Y', 4))
            self._tiles.add(Tile(' ', 0))
        for _ in range(3):
            self._tiles.add(Tile('G', 2))
        for _ in range(4):
            self._tiles.add(Tile('D', 2))
            self._tiles.add(Tile('L', 1))
            self._tiles.add(Tile('S', 1))
            self._tiles.add(Tile('U', 1))
        for _ in range(6):
            self._tiles.add(Tile('N', 1))
            self._tiles.add(Tile('R', 1))
            self._tiles.add(Tile('T', 1))
        for _ in range(8):
            self._tiles.add(Tile('O', 1))
        for _ in range(9):
            self._tiles.add(Tile('A', 1))
            self._tiles.add(Tile('I', 1))
        for _ in range(12):
            self._tiles.add(Tile('E', 1))

    def draw_tiles(self, num_tiles):
        # TODO: randomize draw
        drawn_tiles = []
        for _ in range(max(num_tiles, len(self._tiles))):
            drawn_tiles.append(self._tiles.pop())
        return drawn_tiles

    def exchange_tiles(self, tiles):
        if len(tiles) > len(self._tiles):
            raise NotEnoughTilesException()

        drawn_tiles = self.draw_tiles(len(tiles))
        for x in tiles:
            self._tiles.add(x)
        return drawn_tiles
