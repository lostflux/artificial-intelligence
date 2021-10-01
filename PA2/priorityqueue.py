#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""This module implements a priority queue.
"""
__author__ = "Amittai"
__copyright__ = "Copyright 2021"
__credits__ = ["Amittai"]
__email__ = "Amittai.J.Wekesa.24@dartmouth.edu"
__github__ = "@siavava"

from heapq import heappush, heappop

class PriorityQueue(object):
    """A priority queue implementation using a heap.
    """
    def __init__(self):
        self._heap = list()

    def __len__(self):
        return len(self._heap)

    def __str__(self):
        return str(self._heap)
    
    def __bool__(self):
        """Check if the queue is NOT empty.
        """
        return not self.is_empty()

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
    