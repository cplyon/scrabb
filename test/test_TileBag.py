#!/usr/bin/env python3
#
# Scrabble Game Tests
# Author: Chris Lyon
# Contact: chris@cplyon.ca

import unittest
from scrabb.tile import Tile
from scrabb.tilebag import NotEnoughTilesException, TileBag


class TileBagTest(unittest.TestCase):

    FAKE_TILE = Tile('*', 1)

    def setUp(self):
        pass

    def test_len(self):
        tb = TileBag()
        self.assertEqual(len(tb), 100)

    def test_draw_tiles_full(self):
        tb = TileBag()
        tiles = tb.draw_tiles(7)
        self.assertEqual(len(tiles), 7)
        self.assertEqual(len(tb), 93)

    def test_draw_tiles_empty(self):
        tb = TileBag()
        tb._tiles.clear()
        tiles = tb.draw_tiles(7)
        self.assertEqual(len(tiles), 0)
        self.assertEqual(len(tb), 0)

    def test_exchange_tiles_full(self):
        tb = TileBag()
        to_exchange = [self.FAKE_TILE for _ in range(7)]
        drawn_tiles = tb.exchange_tiles(to_exchange)
        self.assertEqual(len(drawn_tiles), 7)
        self.assertEqual(len(tb), 100)
        self.assertTrue(tb._tiles.is_superset(to_exchange))

    def test_echange_tiles_not_enough(self):
        tb = TileBag()
        tb._tiles.clear()
        to_exchange = [self.FAKE_TILE for _ in range(7)]
        with self.assertRaises(NotEnoughTilesException):
            tb.exchange_tiles(to_exchange)
