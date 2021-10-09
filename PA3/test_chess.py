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
from IterativeDeepeningAI import IterativeDeepeningAI
from ChessGame import ChessGame

from erratum import ( log_error, log_info, log_debug_info )


import sys

import cProfile, pstats, io
from pstats import SortKey

# ... initialize players ...
random_player = RandomAI()
minimax_white = MinimaxAI(2, debug=True)
minimax_black = MinimaxAI(2, maximizing=False, debug=True)

alpha_beta_white = AlphaBetaAI(3, debug=True)
alpha_beta_black = AlphaBetaAI(2, maximizing=False, debug=True)

ids_white = IterativeDeepeningAI(10, debug=True)
ids_black = IterativeDeepeningAI(10, maximizing=False, debug=True)

# start time tracker
pr = cProfile.Profile()
pr.enable()
# ... do something ...


game = ChessGame(alpha_beta_white, random_player)
turns: int = 0
while not game.is_game_over():
    print(game)
    game.make_move()
    turns += 1
print(game)

log_info(f"Checkmate? {game.is_checkmate()}")
log_info(f"Stalemate? {game.is_stalemate()}")
log_info(f"Number of moves: {(turns // 2) + 1}")

pr.disable()
s = io.StringIO()
sortby = SortKey.CUMULATIVE
ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
ps.print_stats()
print(s.getvalue())
