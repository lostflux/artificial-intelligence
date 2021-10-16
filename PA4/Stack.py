#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    This module implements a Stack.
"""
__author__ = "Amittai"
__copyright__ = "Copyright 2021"
__credits__ = ["Amittai"]
__email__ = "Amittai.J.Wekesa.24@dartmouth.edu"
__github__ = "@siavava"

class Stack:
  
    def __init__(self):
        """
        Initializes a new Stack.
        """
        self.items = []
        self.last = 0
        
    def push(self, item):
        """
        Adds an item to the top of the stack.
        """
        self.items.append(item)
        self.last += 1
        
    def pop(self):
        """
            Removes an item from the top of the stack, returns it
        """
        if self.last:
            self.last -= 1
            return self.items.pop()
        
    def peek(self):
        """
            Returns the item on the top of the stack
        """
        if self.last:
            return self.items[self.last - 1]
        
    def __bool__(self):
        """
            Returns True if the stack is empty, False otherwise
        """
        return self.last != 0
    
    def size(self):
        """
            Returns the number of items in the stack
        """
        return self.last