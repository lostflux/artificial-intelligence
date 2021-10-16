#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    This module implements a Queue.
"""
__author__ = "Amittai"
__copyright__ = "Copyright 2021"
__credits__ = ["Amittai"]
__email__ = "Amittai.J.Wekesa.24@dartmouth.edu"
__github__ = "@siavava"

class Queue:
  
    def __init__(self):
        """
        Initializes a new Stack.
        """
        self.items = []
        self.first = 0
        self.last = 0
        
    def add(self, item):
        """
            Adds an item to the top of the stack
        """
        self.items.append(item)
        self.last += 1
        
    def remove(self):
        """
            Removes an item from the top of the stack, returns it
        """
        if self.last > self.first:
            self.fist += 1
            return self.items[self.first - 1]
        
    def peek(self):
        """
            Returns the item on the top of the stack
        """
        if self.first < self.last:
            return self.items[self.first]
        
    def __bool__(self):
        """
            Returns True if the stack is empty, False otherwise
        """
        return self.first < self.last
    
    def size(self):
        """
            Returns the number of items in the stack
        """
        return self.last - self.first