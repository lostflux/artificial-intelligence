#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""This file implements several algorithms for intelligent gameplay, including Minimax AI.
"""
__author__ = "Amittai"
__copyright__ = "Copyright 2021"
__credits__ = ["Amittai"]
__email__ = "Amittai.J.Wekesa.24@dartmouth.edu"
__github__ = "@siavava"

from numpy import inf, log                                       # infinity
from chess import Board                                     # Chess board
import chess                                                # Chess module
from random import shuffle                                  # functiont to shuffle moves.

from erratum import (log_error, log_info, log_debug_info)   # logging functions. see [../erratum.py] for more info.

from MinimaxAI import MinimaxAI

class IterativeDeepeningAI():
    
    
    def __init__(self, max_depth, maximizing=True, timeout=30, debug=False):
        self.maximizing = maximizing
        self.max_depth = max_depth
        self.debug = debug
        self.search_engine: MinimaxAI = MinimaxAI(0, maximizing=maximizing, debug=False)
        self.timeout = timeout
        self.prev_moves = set()
    
    def choose_move(self, board: Board):
        """
            Given a board state, chooses the best move to play next.
        """
        
        # check every move and remember the last move that improves the utility.
        
        
        best_move, best_cost = None, -inf
        counter = self.timeout
        
    
        # iterate over allowed depths.
        for depth in range(1, self.max_depth):
            
            if best_move:
                board.push(best_move)
                new_cost = self.search_engine.minimax(board, depth=depth)
                board.pop()
                
                # First, recheck the best move from previous depth and update cost if it changes.
                if new_cost < best_cost:
                    if self.debug:
                        log_error(f"Move with best score changed score from {best_cost} to {new_cost}.")
                    best_cost = new_cost
            
            # get every possible move and explore it to the current depth.
            for move in board.legal_moves:
                
                # try the move
                board.push(move)
                
                # get the utility of the board after the move.
                cost = self.search_engine.minimax(board, depth=depth)
                
                # check if the move improves the utility.
                # NOTE: we check whether it *matches* the utility, OR if it *betters* the utility.
                # This helps avoid a repetition loop where a sequence of first-occurring moves loop back
                # to each other and the game gets stuck in a loop. 
                # However, we also need to avoid blindly chosing the last move played -- 
                # so we check if the state of the board after the move has been recorded before
                # in the prev_moves set.
                if ( (self.maximizing) and (cost >= best_cost) ) \
                    or ( (not self.maximizing) and (cost <= best_cost) ):
                        
                    # if the cost strictly improves the utility, remember it and log progress.
                    if cost != best_cost:
                        
                        # if debug enabled, print progress
                        if self.debug:
                            if not (best_cost == -inf or best_cost == inf):
                                log_debug_info(f"Depth {depth}; better move found, score shift from {best_cost} to {cost}.")
                            else:
                                log_debug_info(f"First move found at depth {depth}; score = {cost}.")
                        
                        best_move, best_cost = move, cost
                        
                    elif not ((cost == best_cost) and (str(move) in self.prev_moves)):
                        # log_error(f"Depth {depth}; move {move} has same score as previous move {best_move}.")
                        best_move, best_cost = move, cost
                        
                
                # undo the move
                board.pop()
                
                # if the timeout is reached, stop searching other moves. Otherwise, decrement the timeout.
                if counter <= 0: break
                else: counter -= 1
                
            if counter <= 0:
                break
            
            # if debug is enabled, print progress
            if self.debug:
                log_debug_info(f"Depth {depth}, best move: {best_move}, cost: {best_cost}.")
         
        
        # once the best move is found, remember it and return it.
        self.prev_moves.add(str(move))
        
        # print information on chosen best move.
        log_info(f"Iterative Deepening AI recommends move {best_move} with cost {best_cost}")
        
        # return chosen move.
        return best_move