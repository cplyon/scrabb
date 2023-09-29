#! /usr/bin/env python3
#
# Scrabble Game
# Author: Chris Lyon
# Contact: chris@cplyon.ca

from dataclasses import dataclass

@dataclass(frozen=True)
class Tile:
    letter: str
    score: int
