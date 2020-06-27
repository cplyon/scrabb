#! /usr/bin/env python3
#
# Scrabble Game
# Author: Chris Lyon
# Contact: chris@cplyon.ca

class Letter:
    def __init__(self, value, score):
        self.value = value
        self.score = score

    def __str__(self):
        print("{0},{1}".format(self.value, self.score))
