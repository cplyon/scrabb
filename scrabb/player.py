#! /usr/bin/env python3
#
# Scrabble Game
# Author: Chris Lyon
# Contact: chris@cplyon.ca

from dataclasses import dataclass
from .tile import Tile


@dataclass
class Player:
    name: str
    score: int = 0
    rack: list[Tile] = []
