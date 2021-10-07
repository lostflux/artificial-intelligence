#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    This module implements an algorithm to randomly generate Chess moves.
"""
__author__ = "Amittai"
__copyright__ = "Copyright 2021"
__credits__ = ["Amittai", "Alberto Quattrini Li"]
__email__ = "Amittai.J.Wekesa.24@dartmouth.edu"
__github__ = "@siavava"

import chess
import random
from time import sleep

class RandomAI():
    def __init__(self):
        pass

    def choose_move(self, board):
        moves = list(board.legal_moves)
        move = random.choice(moves)
        sleep(1)   # I'm thinking so hard.
        print("Random AI recommending move " + str(move))
        return move
