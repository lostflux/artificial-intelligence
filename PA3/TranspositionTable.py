#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    This module implements a Transposition Table.
"""
__author__ = "Amittai"
__copyright__ = "Copyright 2021"
__credits__ = ["Amittai"]
__email__ = "Amittai.J.Wekesa.24@dartmouth.edu"
__github__ = "@siavava"

from chess import Board, Move

class TranspositionTable(object):
    def __init__(self):
        self.data: dict = {}
        self.len = 0
        
    def __bool__(self):
        return self.len != 0
        
    def __getitem__(self, key):
        return self.data.get(str(key), None)
    
    def __contains__(self, key):
        """Check if the table contains an item.
        """
        if str(key) in self.data:
            return True
        
        return False
    
    def __setitem__(self, key, value):
        self.data[str(key)] = value
        self.len += 1
       
    def __str__(self):
        return str(self.data)
    
    def __len__(self):
        return self.len
    
    # def zobrist_hash(self, board: Board):
    #     """Return the Zobrist hash of a board.
    #     """
    #     hash_value = 0
    #     for square in range(64):
    #         piece = board.piece_at(square)
    #         if piece:
    #             hash_value ^= self.zobrist_piece_table[piece.piece_type][square]
    
    