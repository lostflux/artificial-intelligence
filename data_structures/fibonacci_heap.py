#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    A naive Fibonacci Tree.
"""
__author__ = "Amittai"
__copyright__ = "Copyright 2021"
__credits__ = ["Amittai"]
__email__ = "Amittai.J.Wekesa.24@dartmouth.edu"
__github__ = "@siavava"

from linked_list import LinkedList
from binary_tree import BinaryTree
from typing import TypedDict

class FibonacciHeapNode():
    def __init__(self, item, score):
        self.__item = item
        self.__score = score
        self.__size = 1
        self.__next = LinkedList()
        
    def score(self):
        return self.__score
    
    def size(self):
        return self.__size
        
    def __update_min(self, node):
        assert isinstance(node, FibonacciHeapNode)
        assert self.__score is not None
        self.__score = min(self.__score, node.__score)
        
    def insert(self, node):
        self.__next.append(node)
        self.__size += node.__size
        self.__update_min(node)
        
    def merge(self, other_node):
        self.insert(other_node)
        return self
        
    @staticmethod
    def merge(node_1, node_2):
        assert isinstance(node_1, FibonacciHeapNode)\
            and isinstance(node_2, FibonacciHeapNode)
        if node_1 <= node_2:
            node_1.insert(node_2)
            return node_1
        else:
            node_2.insert(node_1)
            return node_2
            
    def __gt__(self, other):
        return self.__score > other.__score
    
    def __ge__(self, other):
        return self.__score >= other.__score
    
    def __eq__(self, other):
        return self.__score == other.__score
    
    def __ne__(self, other):
        return self.__score != other.__score
    
    def __le__(self, other):
        return self.__score <= other.__score
    
    def __lt__(self, other):
        return self.__score < other.__score
    
    def __hash__(self):
        return hash(self.__item)
    
    def __str__(self):
        return f"{self.__item}: {self.__score}"
    
    def __iter__(self):
        return iter(self.__next)
    
class FibonacciHeap(object):
    """
        A Fibonacci Heap implementation.
    """
    def __init__(self):
        self.__nodes = LinkedList()
        self.__min = None
        self.__size = 0
        
    def size(self):
        return self.__size

    def insert(self, item, score):
        """
            Insert a key into the Fibonacci Heap.
        """
        node = FibonacciHeapNode(item, score)
        self.__size += 1
        self.update_min(node)
        self.__nodes.append(node)
                
    def update_min(self, node):
        if self.__min is None: 
            self.__min: FibonacciHeapNode = node
        else:
            self.__min = min(self.__min, node)

    def extract__min(self):
        """
            Extract the __minimum key from the Fibonacci Heap.
        """
        if self.__min is None:
            return None
        
        min_node = self.__min
        for next_node in min_node:
            self.__nodes.append(next_node)
        self.__heapify()
        return min_node.item
    
    def __index(self):
        sizes = dict[int, set]()
        for node in self:
            assert isinstance(node, FibonacciHeapNode)
            size = node.size()
            if size not in sizes:
                sizes[size] = set()
            sizes[size].add(node)
        return sizes
    
    def __heapify(self):
        sizes = self.__index()
        size = 1
        while size < self.size():
            if size in sizes:
                while sizes[size] > 1:
                    node_1: FibonacciHeapNode = sizes[size].pop()
                    node_2: FibonacciHeapNode = sizes[size].pop()
                    self.__nodes.remove(node_1)
                    self.__nodes.remove(node_2)
                    
                    merged = FibonacciHeapNode.merge(node_1, node_2)
                    self.__nodes.append(merged)
                    new_size = 2 * size
                    if new_size not in sizes:
                        sizes[new_size] = set()
                    sizes[new_size].add(merged)
                for node in sizes[size]:
                    for next_node in node:
                        self.__nodes.append(next_node)
            size += 1
            
        

    def decrease_key(self, node, new_key):
        """
            Decrease the key of a node.
        """
        if new_key > node.key:
            return
        node.key = new_key
        if node.parent is not None and node.key < node.parent.key:
            node.cut()
            node.parent.cascading_cut()

    def delete(self, node):
        """
            Delete a node from the Fibonacci Heap.
        """
        self.decrease_key(node, -float("inf"))
        self.extract___min()

    def __str__(self):
        """
            String representation of the Fibonacci Heap.
        """
        if self.__min is None:
            return "Empty Fibonacci Heap"
        return str(self.__min)

    def __repr__(self):
        """
            String representation of the Fibonacci Heap.
        """
        pass
