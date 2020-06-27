#! /usr/bin/env python3
#
# Scrabble Game
# Author: Chris Lyon
# Contact: chris@cplyon.ca

from .letter import Letter
from collections_extended import bag


class NotEnoughLettersException(Exception):
    pass


class LetterBag:

    def __init__(self):
        self._letters = bag()

    def __len__(self):
        return len(self._letters)

    def populate_letters(self):
        self._letters.clear()
        self._letters.add(Letter('J', 8))
        self._letters.add(Letter('K', 5))
        self._letters.add(Letter('Q', 10))
        self._letters.add(Letter('X', 8))
        self._letters.add(Letter('Z', 10))
        for _ in range(2):
            self._letters.add(Letter('B', 3))
            self._letters.add(Letter('C', 3))
            self._letters.add(Letter('F', 4))
            self._letters.add(Letter('H', 4))
            self._letters.add(Letter('M', 3))
            self._letters.add(Letter('P', 3))
            self._letters.add(Letter('V', 4))
            self._letters.add(Letter('W', 4))
            self._letters.add(Letter('Y', 4))
            self._letters.add(Letter(' ', 0))
        for _ in range(3):
            self._letters.add(Letter('G', 2))
        for _ in range(4):
            self._letters.add(Letter('D', 2))
            self._letters.add(Letter('L', 1))
            self._letters.add(Letter('S', 1))
            self._letters.add(Letter('U', 1))
        for _ in range(6):
            self._letters.add(Letter('N', 1))
            self._letters.add(Letter('R', 1))
            self._letters.add(Letter('T', 1))
        for _ in range(8):
            self._letters.add(Letter('O', 1))
        for _ in range(9):
            self._letters.add(Letter('A', 1))
            self._letters.add(Letter('I', 1))
        for _ in range(12):
            self._letters.add(Letter('E', 1))

    def draw_letters(self, num_letters):
        # TODO: randomize draw
        drawn_letters = []
        for _ in range(max(num_letters, len(self._letters))):
            drawn_letters.append(self._letters.pop())
        return drawn_letters

    def exchange_letters(self, letters):
        if len(letters) > len(self._letters):
            raise NotEnoughLettersException()

        drawn_letters = self.draw_letters(len(letters))
        for x in letters:
            self._letters.add(x)
        return drawn_letters
