#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    This file implements the ALpha-Beta search algorithm for intelligent gameplay.
"""
__author__ = "Amittai"
__copyright__ = "Copyright 2021"
__credits__ = ["Amittai"]
__email__ = "Amittai.J.Wekesa.24@dartmouth.edu"
__github__ = "@siavava"

from numpy import inf                                       # infinity
from chess import Board                                     # Chess board
import chess                                                # Chess module

from erratum import (log_error, log_info, log_debug_info)   # logging functions. see [../erratum.py] for more info.

class AlphaBetaAI():
    """
        A Chess AI that uses Alpha-Beta pruning with the Minimax algorithm to search for the best move.
        Given an optimal opponent, this method *should* return the best worst-case options.
        However, that is limited by the search depth and the algorithm 
        might not be able to see as far down the road as it would
        in a game with less branching than Chess. 
    """
    
    def __init__(self, depth: int, maximizing=True, debug=False):
        """
            Constructor.
            :arg `depth`: maximum search depth.
            :arg `maximizing` [optional]: should be explicitly set to False
            if the goal is to minimize (not maximize) the heuristic. 
        """
        self.depth: int = depth
        self.maximizing: bool = maximizing
        self.debug: bool = debug
        self.pruned_branches: int = 0
        self.prev_moves = set()

    def choose_move(self, board: Board):
        """
            Given a board state, chooses the best move to play next.
        """
        
        # get all moves, initialize best utility to neg infinity.
        best_move = None
        best_cost = -inf if self.maximizing else inf
        
        # check every move and remember the last move that improves the utility.
        for move in board.legal_moves:
            
            # try the move.
            board.push(move)
            cost = self.alpha_beta_search(board)
                
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
                            log_debug_info(f"Better move found, score shift from {best_cost} to {cost}.")
                        else:
                            log_debug_info(f"First move found, score = {cost}.")
                    
                    best_move, best_cost = move, cost
                    
                elif not ((cost == best_cost) and (str(move) in self.prev_moves)):
                    best_move, best_cost = move, cost
            
            # undo the move.
            board.pop()
            
        # once the best move is found, remember it and return it.
        self.prev_moves.add(str(best_move))
        
        # print information on chosen best move.
        log_info(f"\nAlpha-Beta AI recommending move = {best_move}, move score = {best_cost}\n")
        
        # return chosen move.
        return best_move
    
    def cutoff_test(self, board: Board, depth: int):
        """
            Given a board state and a search depth, determines whether
            the search should go on or the search should be cut off.
            :arg board: a Chess board object.
            :arg depth: integer repsesenting how far deeper the search should go on.
            
        """
        return (depth == 0) or (board.is_game_over())
    
    def alpha_beta_search(self, board: Board):
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
            return self.max_value(board, self.depth, -inf, inf)
        
        # otherwise, return the min_value.
        else:
            return self.min_value(board, self.depth, -inf, inf)
            
    
    def max_value(self, board, depth, best, worst):
        """
            Given a board state, finds the maximum value for that state.
        """
            
        # if cutoff point has been reached, evaluate the state of the board.
        if self.cutoff_test(board, depth):
            value = self.evaluate(board)
            return value
        
        # otherwise, recursively find the max of min for each next state,
        # remembering the state that gives the best outcome.
        #
        # NOTE: If the value is greater than or equal to the worst value from the other search nodes,
        # since we know the next player will be minimizing (and we are maximizing here),
        # we can prune the remaining searches because they are insignificant.
        #
        # otherwise, we:
        #   1. save the value to the transposition table, 
        #   2. update the best value seen yet, 
        #   3. and continue the looping search on other next states.
        else:
            
            highest_value = -inf
            
            for move in board.legal_moves:
                board.push(move)
                highest_value = max(highest_value, self.min_value(board, depth-1, best, worst))
                board.pop()
                
                if highest_value >= worst:
                    self.pruned_branches += 1
                    return highest_value
                    
                else:
                    best = max(best, highest_value)
            
            return highest_value
    
    def min_value(self, board, depth, best, worst):
        """
            Given a board state, finds the minimum value for that state.
        """
            
        # if cutoff point has been reached, evaluate the value of the board.
        if self.cutoff_test(board, depth):
            value = self.evaluate(board)
            return value
        
        # otherwise, recursively find the max of min for each next state,
        # remembering the state that gives the best outcome.
        #
        # NOTE: If the value is less than or equal to the best value from the other search nodes,
        # since we know the next player will be maximizing (and we are minimizing here),
        # we can prune the remaining searches because they are insignificant.
        #
        # otherwise, we:
        #   1. save the value to the transposition table, 
        #   2. update the worst value seen yet, 
        #   3. and continue the looping search on other next states.
        else: 
            lowest_value = inf
            
            for move in board.legal_moves:
                board.push(move)
                lowest_value = min(lowest_value, self.max_value(board, depth-1, best, worst))
                board.pop()
                if lowest_value <= best:
                    self.pruned_branches += 1
                    return lowest_value
                    
                else:
                    worst = min(worst, lowest_value)
                    
            return lowest_value


####################################################################################
####################################################################################
########################### Board Evaluation Functions #############################
####################################################################################
####################################################################################

    
    def evaluate(self, board: Board):
        """
            Evaluate a Chess position and determine its disirability.
        """

        # if the game is over, return infinity, neg infinity, or zero
        # depending on whether the game has been won, lost, or drawn.
        if board.is_game_over():
            return self.end_status(board)
            
        # if the game is not yet over, parse the pieces on the board
        # to determine the value of the value of the state.
        white = self.parse_color(board, chess.WHITE)
        black = self.parse_color(board, chess.BLACK)
        return white - black
    
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

    @staticmethod
    def parse_color(board: Board, suit):
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
    