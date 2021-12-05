#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""This module implements a priority queue.
"""
__author__ = "Amittai"
__copyright__ = "Copyright 2021"
__credits__ = ["Amittai"]
__email__ = "Amittai.J.Wekesa.24@dartmouth.edu"
__github__ = "@siavava"

from heapq import ( heappush, heappop )

class PriorityQueue(object):
    """
        A priority queue implementation using a heap.
        This implementation uses `heapq`'s `heappush` and `heappop` functions
        to maintain efficient heap operations.
    """
    def __init__(self):
        self._heap = list()

    def __len__(self):
        """
            Return the length of the queue.
        """
        return len(self._heap)

    def __str__(self):
        """
            Return a string representation of the queue.
        """
        return str(self._heap)
    
    def __bool__(self):
        """Check if the queue is NOT empty.
        """
        return not self.is_empty()
    
    def __iter__(self):
        """Return an iterator for the queue.
        """
        return iter(self._heap)
    
    def __contains__(self, item):
        """Check if the queue contains an item.
        """
        return item in self._heap
    
    def __getitem__(self, index):
        """Get an item from the queue.
        """
        return self._heap[index]
    
    def __reversed__(self):
        """Return a reversed iterator for the queue.
        """
        return reversed(self._heap)
    
    def __repr__(self):
        """Return a string representation of the queue.
        """
        return repr(self._heap)

    def push(self, item):
        """Push an item with a priority to the queue.
        """
        heappush(self._heap, item)

    def pop(self):
        """Pop the item with the highest priority from the queue.
        """
        if not self._heap:
            raise IndexError('Pop from empty queue.')
        
        return heappop(self._heap)
    
    def is_empty(self):
        """Check if the queue is empty.
        """
        if not self._heap:
            return True
        return False
    
    def peek(self):
        """Get the item with the highest priority from the queue.
        """
        if not self._heap:
            raise IndexError('Peek from empty queue.')
        
        return self._heap[0]
    
    def clear(self):
        """Clear the queue.
        """
        self._heap = []
