#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""This module is a driver function for the Chess Game.
"""
__author__ = "Amittai"
__copyright__ = "Copyright 2021"
__credits__ = ["Amittai"]
__email__ = "Amittai.J.Wekesa.24@dartmouth.edu"
__github__ = "@siavava"

# pip3 install python-chess


import chess
from RandomAI import RandomAI
from HumanPlayer import HumanPlayer
from MinimaxAI import MinimaxAI
from AlphaBetaAI import AlphaBetaAI
from ChessGame import ChessGame


import sys

import cProfile, pstats, io
from pstats import SortKey


pr = cProfile.Profile()
pr.enable()
# ... do something ...


# player1 = HumanPlayer()
# player1 = MinimaxAI(3, debug=True)
player1 = AlphaBetaAI(3, debug=True)
player2 = RandomAI()


game = ChessGame(player1, player2)
turns: int = 0
while not game.is_game_over():
    print(game)
    game.make_move()
    turns += 1
print(game)

print(f"Checkmate? {game.is_checkmate()}")
print(f"Stalemate? {game.is_stalemate()}")
print(f"Number of moves: {(turns // 2) + 1}")


# print(hash(str(game.board)))

pr.disable()
s = io.StringIO()
sortby = SortKey.CUMULATIVE
ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
ps.print_stats()
print(s.getvalue())
