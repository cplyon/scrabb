#! /usr/bin/env python3
#
# Scrabble Game
# Author: Chris Lyon
# Contact: chris@cplyon.ca

class Tile:
    def __init__(self, letter, score):
        self.letter = letter
        self.score = score

    def __str__(self):
        print("{0},{1}".format(self.letter, self.score))
