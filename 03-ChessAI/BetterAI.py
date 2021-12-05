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
from erratum import (log_error, log_info, log_debug_info)   # logging functions. see [../erratum.py] for more info.
from EnhancedAlphaBetaAI import EnhancedAlphaBetaAI         # A/B AI for searching.
from EnhancedAlphaBetaAI import OrderedMove

from priorityqueue import PriorityQueue                    # Priority queue for move reordering.
class BetterAI():
    """
        A Chess AI that uses Alpha-Beta pruning with the Minimax algorithm to search for the best move.
        Given an optimal opponent, this method *should* return the best worst-case options.
        However, that is limited by the search depth and the algorithm 
        might not be able to see as far down the road as it would
        in a game with less branching than Chess.
        
        Rather than blindly follow all moves in searching,
        `BetterAI` will first check the state of the board 
        immediately after the moves to determine the moves likely to be best,
        and only follow the top *move_count* moves 
        where X is a value specified in the constructor, defaulted to 7.
        
        This module behavs in the same way as Iterative Deepening, but uses the EnhancedAlphaBetaAI module as a search engine.
    """
    
    
    def __init__(self, max_depth=7, maximizing=True, move_count=4, timeout=15, debug=False):
        """
            Constructor.
            :arg max_depth: the maximum depth to search to.
            :arg maximizing: whether to maximize or minimize the utility.
            :arg move_count: the number of moves to follow.
            :arg timeout: the *maximum* number of search operations to do.
            :arg debug: whether to print debug information.
        """
        self.maximizing = maximizing
        self.max_depth = max_depth
        self.debug = debug
        self.search_engine: EnhancedAlphaBetaAI = \
            EnhancedAlphaBetaAI(0, maximizing=self.maximizing, memoized=False, move_count=move_count, debug=debug)
        self.prev_moves = set()
        self.move_count = move_count
        self.timeout = timeout
       
     
    def choose_move(self, board: Board):
        """
            Given a board state, chooses the best move to play next.
        """        
        
        # initialize the best move and cost.
        best_move, best_cost = None, -inf
        counter = self.timeout
        
        # iterate over allowed depths.
        for depth in range(1, self.max_depth):
            
            if best_move:
                board.push(best_move)
                new_cost = self.search_engine.alpha_beta_search(board, depth=depth)
                board.pop()
                
                # First, recheck the best move from previous depth and update cost if it changes.
                if new_cost != best_cost:
                    if self.debug:
                        log_error(f"Move {best_move} changed in score from {best_cost} to {new_cost}.")
                    best_cost = new_cost
                    
            ordered_moves = self.search_engine.reorder_moves(board, board.legal_moves)
            
            # get every possible move and explore it to the current depth.
            
            move_count = self.move_count
            while move_count > 0 and ordered_moves:
                
                move_count -= 1
                move = ordered_moves.pop().move
                
                # try the move
                board.push(move)
                
                # get the utility of the board after the move.
                cost = self.search_engine.alpha_beta_search(board, depth=depth)
                
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
                        best_move, best_cost = move, cost
                        
                
                # undo the move
                board.pop()
                
                # if the timeout is reached, stop searching other moves. Otherwise, decrement the timeout.
                if counter <= 0: break
                else: counter -= 1
                
            
            # if debug is enabled, print progress
            if self.debug:
                log_debug_info(f"Depth {depth}, best move: {best_move}, cost: {best_cost}.")
                
            if counter <= 0: break
         
        
        # once the best move is found, remember it and return it.
        self.prev_moves.add(str(move))
        
        # print information on chosen best move.
        log_info(f"Better AI recommends move {best_move} with cost {best_cost}")
        
        # return chosen move.
        return best_move