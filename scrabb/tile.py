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
        return f"({self.letter},{self.score})"
