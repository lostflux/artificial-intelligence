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

class Node:
    def __init__(self, data, next):
        self.data = data
        self.next = next
        

class Queue:
  
    def __init__(self):
        """
        Initializes a new Stack.
        """
        self.head = None
        self.size = 0
        
    def push(self, item):
        """
            Adds an item to the top of the stack
        """
        new_node = Node(item, self.head)
        self.head = new_node
            
        self.size += 1
        
    def pop(self):
        """
            Removes an item from the top of the stack, returns it
        """
        if self.head:
            item = self.head.data
            self.head = self.head.next
            self.size -= 1
            return item
        
        raise IndexError("Empty stack!")
        
    def peek(self):
        """
            Returns the item on the top of the stack
        """
        if self.head:
            return self.head.data
        
        return None
        
    def __bool__(self):
        """
            Returns True if the stack is empty, False otherwise
        """
        return self.size != 0
    