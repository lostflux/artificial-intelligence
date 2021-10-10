#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""This file implements several algorithms for intelligent gameplay, including Miniman AI.
"""
__author__ = "Amittai"
__copyright__ = "Copyright 2021"
__credits__ = ["Amittai"]
__email__ = "Amittai.J.Wekesa.24@dartmouth.edu"
__github__ = "@siavava"

from numpy import inf                                       # infinity
from chess import Board                                     # Chess board
import chess                                                # Chess module
from random import shuffle                                  # functiont to shuffle moves.

from erratum import (log_error, log_info, log_debug_info)   # logging functions. see [../erratum.py] for more info.

from MinimaxAI import MinimaxAI

class IterativeDeepeningAI():
    
    
    def __init__(self, max_depth=5, maximizing=True, debug=False):
        self.maximizing = maximizing
        self.max_depth = max_depth
        self.debug = debug
        self.search_engine: MinimaxAI = MinimaxAI(0, maximizing=self.maximizing, debug=debug)
        
       
     
    def choose_move(self, board: Board):
        """
            Given a board state, chooses the best move to play next.
        """
        
        # check every move and remember the last move that improves the utility.
        best_move, best_cost = None, -inf
        for depth in range(self.max_depth):
            
            for move in board.legal_moves:
                # try the move
                board.push(move)
                
                # get the utility of the move
                cost = self.search_engine.minimax(board, depth, self.max_depth, self.maximizing)
                
                # check if the move improves the utility
                if ( (self.maximizing) and (cost > best_cost) ) \
                    or ( (not self.maximizing) and (cost < best_cost) ):
                    best_move, best_cost = move, cost
                
                # undo the move
                board.pop()
            
            if self.debug:
                log_debug_info(f"Depth {depth}, best move: {best_move}, cost: {best_cost}.")
         
        log_info(f"Iterative Deepening AI recommends move {best_move} with cost {best_cost}")   
        return best_move