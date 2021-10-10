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
        self.data: dict  ={}
        
    def __bool__(self):
        return len(self.data) != 0
        
    def __getitem__(self, key):
        return self.data.get(hash(str(key)), None)
    
    def __contains__(self, key):
        """Check if the table contains an item.
        """
        if hash(str(key)) in self.data:
            return True
        
        return False
    
    def __setitem__(self, key, value):
        self.data[hash(str(key))] = value
       
    def __str__(self):
        return str(self.data)
    
    def __len__(self):
        return len(self.data)
    
    # @staticmethod
    # def zobrist_hash(board: Board):
    #     hash_value = 0
    #     for piece in board.pieces:
    
    