#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""This module implements apriority queue.
"""
__author__ = "Amittai"
__copyright__ = "Copyright 2021"
__credits__ = ["Amittai", "Alberto Quattrini Li"]
__email__ = "Amittai.J.Wekesa.24@dartmouth.edu"
__github__ = "@siavava"

from heapq import heappush, heappop

class PriorityQueue(object):
    """A priority queue implementation using a heap.
    """
    def __init__(self):
        self._heap = []

    def __len__(self):
        return len(self._heap)

    def __str__(self):
        return str(self._heap)

    def push(self, item):
        """Push an item with a priority to the queue.
        """
        heappush(self._heap, item)

    def pop(self):
        """Pop the item with the highest priority from the queue.
        """
        return heappop(self._heap)
    
    def is_empty(self):
        """Check if the queue is empty.
        """
        return len(self._heap) == 0