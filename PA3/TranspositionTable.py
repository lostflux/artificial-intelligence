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
    
    # @staticmethod
    # def zobrist_hash(board: Board):
    #     hash_value = 0
    #     for piece in board.pieces:
    
    