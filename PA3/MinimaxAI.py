#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""This file implements several algorithms for intelligent gameplay, including Miniman AI.
"""
__author__ = "Amittai"
__copyright__ = "Copyright 2021"
__credits__ = ["Amittai"]
__email__ = "Amittai.J.Wekesa.24@dartmouth.edu"
__github__ = "@siavava"

from numpy import inf
import chess

class MinimaxAI():
    def __init__(self, depth):
        self.depth = depth

    def choose_move(self, board):
        best_move = None
        best_value = -inf
        all_moves = board.legal_moves
        for move in all_moves:
            if not best_move:
                best_move = move
                continue
            
            board.push(move)
            score = self.minimax(board, depth=self.depth, maximizing=True)
            if score > best_value:
                best_move = move
                best_value = score
            board.pop()
        return best_move
    
    def cutoff_test(self, board):
        all_moves = list(board.legal_moves)
        return len(all_moves) == 0
    
    def minimax(self, board, depth=10, maximizing=True):
        if depth == 0 or self.cutoff_test(board):
            return self.evaluate(board)
        if maximizing:
            return self.max_value(board, depth)
        else:
            return self.min_value(board, depth)

    def evaluate(self, board):
        white = self.parse_color(board, chess.WHITE)
        black = self.parse_color(board, chess.BLACK)
        return white - black
    
    def parse_color(self, board, suit):
        
        val = len(board.pieces(chess.PAWN, suit))
        val += 3 * (len(board.pieces(chess.KNIGHT, suit)))
        val += 3 * (len(board.pieces(chess.BISHOP, suit)))
        val += 5 * len(board.pieces(chess.ROOK, suit))
        val += 9 * len(board.pieces(chess.QUEEN, suit))
        
        return val
            
    
    def max_value(self, board, depth):
        if depth == 0 or self.cutoff_test(board):
            return self.evaluate(board)
        highest_value = -inf
        for move in board.legal_moves:
            board.push(move)
            highest_value = max(highest_value, self.min_value(board, depth - 1))
            board.pop()
        return highest_value
    
    def min_value(self, board, depth):
        if depth == 0 or self.cutoff_test(board):
            return self.evaluate(board)
        lowest_value = inf
        for move in board.legal_moves:
            board.push(move)
            lowest_value = min(lowest_value, self.max_value(board, depth - 1))
            board.pop()
        return lowest_value
