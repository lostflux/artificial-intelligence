#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""This file implements several algorithms for intelligent gameplay, including Miniman AI.
"""
__author__ = "Amittai"
__copyright__ = "Copyright 2021"
__credits__ = ["Amittai"]
__email__ = "Amittai.J.Wekesa.24@dartmouth.edu"
__github__ = "@siavava"

from numpy import inf                               # infinity
from chess import Board                             # Chess board
import chess                                        # Chess module
from TranspositionTable import TranspositionTable
from random import shuffle

class MinimaxAI():
    """
        A Chess AI that uses the Minimax algorithm to search for the best move.
        Given an optimal opponent, this method *should* return the best worst-case options.
        However, that is limited by the search depth and the algorithm 
        might not be able to see as far down the road as it would
        in a game with less branching than Chess. 
    """
    def __init__(self, depth, maximizing=True, debug=False):
        """
            Constructor.
            :arg `depth`: maximum search depth.
            :arg `maximizing` [optional]: should be explicitly set to False
            if the goal is to minimize (not maximize) the heuristic. 
        """
        self.depth: int = int(depth)
        self.seen_states: TranspositionTable = TranspositionTable()
        self.maximizing: bool = maximizing
        self.debug: bool = debug

    def choose_move(self, board: Board):
        """
            Given a board state, chooses the best move to play next.
        """
        
        # get all moves, initialize best utility to neg infinity.
        best_move = None
        best_value = -inf
        all_moves = list(board.legal_moves)
        shuffle(all_moves)
        
        # check every move and remember the last move that improves the utility.
        for move in all_moves:
            
            board.push(move)
            if board in self.seen_states:
                score = self.seen_states[str(board)]
            
            else:
                score = self.minimax(board)
                
                ######### if debug flag is set, print debug info. #########
                if self.debug:
                    print(f"move = {move}, minimax = {score}")
                self.seen_states[board] = score
                
            if score > best_value:
                best_move = move
                best_value = score
            
            board.pop()
        
        ######### if debug flag is set, print debug info. #########
        if self.debug:
            print(f"Transposition Table size: {len(self.seen_states)}")
            
        print("Minimax AI recommending move " + str(best_move))
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

    def evaluate(self, board: Board):
        """
            Evaluate a Chess position and determine its disirability.
        """

        # if the game is over, return infinity, neg infinity, or zero
        # depending on whether the game has been won, lost, or drawn.
        if board.is_game_over():
            result: str = board.outcome().result()
            if result == "1-0":
                return inf
            elif result == "1/2-1/2":
                return 0
            else:
                return -inf
            
        # if the game is nto yet over, parse the pieces on the board
        # to determine the value of the value of the state.
        white = self.parse_color(board, chess.WHITE)
        black = self.parse_color(board, chess.BLACK)
        return white - black
    
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
            
    
    def max_value(self, board, depth):
        """
            Given a board state, finds the maximum value for that state.
        """

        # if state has been seen already, get the value from transposition table.
        if str(board) in self.seen_states:
                return self.seen_states[board]
            
        # otherwise, if cutoff point has been reached, evaluate the value of the board.
        elif self.cutoff_test(board, depth):
            return self.evaluate(board)
        
        # otherwise, recursively find the max of min for each next state,
        # remembering the state that gives the best outcome.
        else:
            highest_value = -inf
            all_moves = list(board.legal_moves)
            # shuffle(all_moves)
            for move in all_moves:
                board.push(move)
                highest_value = max(highest_value, self.min_value(board, depth-1))
                board.pop()
            self.seen_states[board] = highest_value  
            
            return highest_value
    
    def min_value(self, board, depth):
        """
            Given a board state, finds the minimum value for that state.
        """
        
        # if state has been seen already, get the value from transposition table.
        if str(board) in self.seen_states:
                return self.seen_states[board]
            
        # otherwise, if cutoff point has been reached, evaluate the value of the board.
        elif self.cutoff_test(board, depth):
            return self.evaluate(board)
        
        # otherwise, recursively find the max of min for each next state,
        # remembering the state that gives the best outcome.
        else: 
            lowest_value = inf
            all_moves = list(board.legal_moves)
            # shuffle(all_moves)
            for move in all_moves:
                board.push(move)
                lowest_value = min(lowest_value, self.max_value(board, depth-1))
                board.pop()
            self.seen_states[board] = lowest_value
            return lowest_value
