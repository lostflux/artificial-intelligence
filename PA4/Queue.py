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

class Node:
    def __init__(self, data, next=None, previous=None):
        self.data = data
        self.next = None
        

class Queue:
  
    def __init__(self):
        """
        Initializes a new Queue.
        """
        self.head = None
        self.tail = None
        self.size = 0
        
    def add(self, item):
        """
            Adds an item to the back of the queue.
        """
        if not self.size:
            self.head = Node(item)
            self.tail = self.head
            
        else:
            new_node = Node(item)
            self.tail.next = new_node
            self.tail = new_node
            
        self.size += 1
        
    def remove(self):
        """
            Removes item from the front of the queue.
        """
        if self.head:
            item = self.head.data
            self.head = self.head.next
            self.size -= 1
            return item
        
        return None
        
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
    
    def __len__(self):
        """
            Returns the size of the stack
        """
        return self.size
    