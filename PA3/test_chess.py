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
from EnhancedAlphaBetaAI import EnhancedAlphaBetaAI
from BetterAI import BetterAI
from erratum import ( log_error, log_info, log_debug_info )
import sys

import cProfile, pstats, io
from pstats import SortKey

def main():
    # ... initialize players ...
    random_player = RandomAI()
    minimax_white = MinimaxAI(2, debug=True)
    minimax_black = MinimaxAI(2, maximizing=False, debug=True)

    alpha_beta_white = AlphaBetaAI(3, debug=True)
    alpha_beta_black = AlphaBetaAI(3, maximizing=False, debug=True)

    # toggle timeout to limit search operations.
    ids_white = IterativeDeepeningAI(7, timeout=50, debug=True)
    ids_black = IterativeDeepeningAI(7, timeout=30, maximizing=False, debug=True)

    # toggle memoized to True to use Transposition Table, 
    # vary move_count to change number of best moves that are considered
    enhanced_alpha_beta_white = EnhancedAlphaBetaAI(5, move_count=4, memoized=False, debug=True)
    enhanced_alpha_beta_black = EnhancedAlphaBetaAI(5, maximizing=False, debug=True)

    better_ai_white = BetterAI(timeout=100, debug=True)
    better_ai_black = BetterAI(timeout=30, maximizing=False, debug=True)



    ######### Initialze game #########
    ###! Unmute one of these definitions to play the game.

    # # minimax
    # game = ChessGame(minimax_white, random_player)
    # game = ChessGame(random_player, minimax_black)
    # game = ChessGame(minimax_white, minimax_black)

    # # alpha beta
    # game = ChessGame(alpha_beta_white, random_player)
    # game = ChessGame(random_player, alpha_beta_black)
    # game = ChessGame(alpha_beta_white, alpha_beta_black)

    # # iterative deepening
    # game = ChessGame(ids_white, random_player)
    # game = ChessGame(random_player, ids_black)
    # game = ChessGame(ids_white, ids_black)

    # # enhanced alpha beta
    game = ChessGame(enhanced_alpha_beta_white, random_player)
    # game = ChessGame(random_player, enhanced_alpha_beta_black)
    # game = ChessGame(enhanced_alpha_beta_white, alpha_beta_black)

    # # better ai (my version with a bunch of changes)
    # game = ChessGame(better_ai_white, random_player)
    # game = ChessGame(random_player, better_ai_black)
    # game = ChessGame(better_ai_white, better_ai_black)

    ## Tests for Transpotition Table
    # enhanced_alpha_beta_white = EnhancedAlphaBetaAI(4, move_count=5, memoized=True, debug=True)
    # game = ChessGame(enhanced_alpha_beta_white, random_player)

    # start time tracker
    pr = cProfile.Profile()
    pr.enable()
    # ... do something ...
    
    ######################## Game Loop #########################
    turns: int = 0
    while not game.is_game_over():
        print(game)
        game.make_move()
        turns += 1
    print(game)

    ######################## End Game Loop #########################

    log_info(f"Checkmate? {game.is_checkmate()}")
    log_info(f"Stalemate? {game.is_stalemate()}")
    log_info(f"Number of moves: {(turns // 2) + 1}")

    pr.disable()
    s = io.StringIO()
    sortby = SortKey.CUMULATIVE
    ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
    ps.print_stats()
    print(s.getvalue())

def test2():
# test minimax and alpha beta move suggestion equality
    
    random_player = RandomAI()
    minimax_white = MinimaxAI(2, debug=True)
    minimax_black = MinimaxAI(2, maximizing=False, debug=True)

    alpha_beta_white = AlphaBetaAI(3, debug=True)
    alpha_beta_black = AlphaBetaAI(3, maximizing=False, debug=True)
    
    game_1 = ChessGame(minimax_white, random_player)
    game_2 = ChessGame(alpha_beta_white, random_player)

    FEN = "r3kb1r/p2p3p/1p4pn/1P2P1q1/2P1b3/NPQ5/5PPP/R3KB1R"
    FEN2 = "r4r2/pb1pk2p/1p4p1/1P6/2PR4/1P3n2/4BP1P/3K4"
    FEN3 = "r4r2/p6p/1p4p1/1Pk5/b4P2/R7/7P/2K5"
    game_1.board.set_fen(FEN3)
    game_2.board.set_fen(FEN3)
    game_1.make_move()
    print("Game 1:\n", game_1)
    game_2.make_move()
    print("Game 2:\n", game_2)
    
if __name__ == "__main__":
    # main()
    test2()
