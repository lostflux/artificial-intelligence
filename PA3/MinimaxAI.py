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

class MinimaxAI():
    """
        A Chess AI that uses the Minimax algorithm to search for the best move.
        Given an optimal opponent, this method *should* return the best worst-case options.
        However, that is limited by the search depth and the algorithm 
        might not be able to see as far down the road as it would
        in a game with less branching than Chess. 
    """
    
    def __init__(self, depth: int, maximizing=True, debug=False):
        """
            Constructor.
            :arg `depth`: maximum search depth.
            :arg `maximizing` [optional]: should be explicitly set to False if you're playing as Black.
            :arg `debug` [optional]: should be explicitly set to True if you want to see debug info.
            if the goal is to minimize (not maximize) the heuristic. 
        """
        self.depth: int = depth
        self.maximizing: bool = maximizing
        self.debug: bool = debug

    def choose_move(self, board: Board, depth=None):
        """
            Given a board state, chooses the best move to play next.
        """
        
        if depth:
            self.depth = int(depth)
        
        # get all moves, initialize best utility to neg infinity.
        best_move = None
        best_value = -inf if self.maximizing else inf
        all_moves = list(board.legal_moves)
        # shuffle(all_moves)
        
        # check every move and remember the last move that improves the utility.
        for move in all_moves:
            
            board.push(move)
            score = self.minimax(board)
            
            #########! if debug flag is set, print debug info. #########
            if self.debug:
                log_debug_info(f"move = {move}, score = {score}")
                
                
                
            if ( (self.maximizing) and (score >= best_value) ) or \
                ( (not self.maximizing) and (score <= best_value)):
                best_move = move
                best_value = score
            
            board.pop()
            
        log_info(f"\nMinimax AI recommending move = {best_move}, move score = {best_value}\n")
        return best_move
    
    def cutoff_test(self, board: Board, depth: int):
        """
            Given a board state and a search depth, determines whether
            the search should go on or the search should be cut off.
            :arg board: a Chess board object.
            :arg depth: integer repsesenting how far deeper the search should go on.
            
        """
        return (depth == 0) or (board.is_game_over())
    
    def minimax(self, board: Board):
        """
            Given a board state, calculate the minimax value of that board state.
            :arg `board`: Chess board state.
            :arg `depth`:
        """
        
        # if cutoff point has been reached, return an evaluation of the board state.
        if self.cutoff_test(board, self.depth):
            return self.evaluate(board)
        
        # otherwise, if the target is to maximize, return the max_value.
        elif self.maximizing:
            return self.max_value(board, self.depth)
        
        # otherwise, return the min_value.
        else:
            return self.min_value(board, self.depth)
        
    @staticmethod
    def end_status(board: Board):
        """
            Determine the desirability of a game end-state.
        """
        
        # if game is not yet over, print error message and return 0.
        if not board.is_game_over():
            log_error("Game is not over yet.")
            return 0
        
        result: str = board.outcome().result()
        if result == "1-0":
            return inf
        elif result == "1/2-1/2":
            return 0
        else:
            return -inf

    def parse_color(self, board: Board, suit):
        """
            Given a board state and a suit, parses the pieces of that suit
            on othe board and returns their total value.
        """
        
        val = len(board.pieces(chess.PAWN, suit))           # Pawns -> value 1
        val += 3 * len(board.pieces(chess.KNIGHT, suit))    # Knights -> value 3
        val += 3 * len(board.pieces(chess.BISHOP, suit))    # Bishops -> value 3
        val += 5 * len(board.pieces(chess.ROOK, suit))      # Rooks -> value 5
        val += 9 * len(board.pieces(chess.QUEEN, suit))     # Queens -> value 9
        
        return val
    
    def evaluate(self, board: Board):
        """
            Evaluate a Chess position and determine its disirability.
        """

        # if the game is over, return infinity, neg infinity, or zero
        # depending on whether the game has been won, lost, or drawn.
        if board.is_game_over():
            return self.end_status(board)
            
        # if the game is nto yet over, parse the pieces on the board
        # to determine the value of the value of the state.
        white = self.parse_color(board, chess.WHITE)
        black = self.parse_color(board, chess.BLACK)
        return white - black
    
    
    def max_value(self, board: Board, depth: int):
        """
            Given a board state, finds the maximum value for that state.
        """
            
        # if cutoff point has been reached, evaluate the value of the board.
        if self.cutoff_test(board, depth):
            value = self.evaluate(board)
            return value
        
        # otherwise, recursively find the max of min for each next state,
        # remembering the best outcome.
        else:
            highest_value = -inf
            all_moves = list(board.legal_moves)
            
            for move in all_moves:
                board.push(move)
                highest_value = max(highest_value, self.min_value(board, depth-1))
                board.pop()
            
            return highest_value
    
    def min_value(self, board, depth):
        """
            Given a board state, finds the minimum value for that state.
        """
            
        # otherwise, if cutoff point has been reached, evaluate the value of the board.
        if self.cutoff_test(board, depth):
            value = self.evaluate(board)
            return value
        
        # otherwise, recursively find the max of min for each next state,
        # remembering the best outcome.
        else: 
            lowest_value = inf
            all_moves = list(board.legal_moves)
            
            for move in all_moves:
                board.push(move)
                lowest_value = min(lowest_value, self.max_value(board, depth-1))
                board.pop()
                
            return lowest_value
