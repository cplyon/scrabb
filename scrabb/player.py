#! /usr/bin/env python3
#
# Scrabble Game
# Author: Chris Lyon
# Contact: chris@cplyon.ca


class Player:

    def __init__(self, name):
        self.name = name
        self.score = 0
        self.rack = []
