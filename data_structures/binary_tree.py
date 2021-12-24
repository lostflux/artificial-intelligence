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

class BinaryTree:
    """Balancing Binary Tree (BST) """
    
    def __init__(self, value=None, left=None, right=None, source=None):
        self.__value = value
        self.__left: BinaryTree = left
        self.__right: BinaryTree = right
        
        if source:
            self.insert_all(source)
        
    def insert(self, value):
        if self.__value is None:
            self.__value = value
        elif value < self.__value:
            if self.__left:
                self.__left.insert(value)
            else:
                self.__left = BinaryTree(value=value)
        else:
            if self.__right:
                self.__right.insert(value)
            else:
                self.__right = BinaryTree(value=value)
                
    def search(self, value):
        if value == self.__value:
            return True
        elif value < self.__value:
            if not self.__left:
                return False
            return self.__left.search(value)
        elif value > self.__value:
            if not self.__right:
                return False
            return self.__right.search(value)
        
    def delete(self, value):
        if value == self.__value:
            if self.__right:
                self.__value = self.__right.min()
                self.__right.delete(self.__value)
            elif self.__left:
                self.__value = self.__left.max()
                self.__left.delete(self.__value)
            else:
                self.__value = None
                
        elif value < self.__value:
            if self.__left:
                self.__left.delete(value)
        else:
            if self.__right:
                self.__right.delete(value)
            
    def min(self):
        node = self
        while node.left:
            node = node.left
        return node.value
            
    def max(self):
        node = self
        while node.right:
            node = node.right
        return node.value
    
    def __check_order(self, flip):
        if flip:
            first, second = self.__right, self.__left
        else:
            first, second = self.__left, self.__right
            
        return first, second
            
    def inorder(self, flip=False):
        
        first, second = self.__check_order(flip)
        
        values = []
        
        if first:
            values += first.inorder(flip)
            
        if self.__value:
            values.append(self.__value)
        
        if second:
            values += second.inorder(flip)
        return values
            
    def preorder(self, flip=False):
        
        first, second = self.__check_order(flip)
        
        values = []
        
        if self.__value:
            values = [self.__value]
        
        if first:
            values += first.preorder(flip)
        if second:
            values += second.preorder(flip)
        return values
            
    def postorder(self, flip=False):
        
        first, second = self.__check_order(flip)
        
        values = []
            
        if first:
            values += first.postorder(flip)
        if second:
            values += second.postorder(flip)
            
        if self.__value:
            values.append(self.__value)
        return values
        
    def rebalance(self):
        """Rebalance the tree"""
        
        if self.__left and self.__right:
            diff = abs(self.__left - self.__right)
            if diff > 1:
                return
            
            values = list(self.inorder())
            self.__init__(source=values)
                
    def insert_all(self, values: list):
        if values:
            mid = len(values) // 2
            print(f"mid: {mid}, values: {values}")
            mid_value = values[mid]
            self.insert(mid_value)
            self.insert_all(values[:mid])
            self.insert_all(values[mid+1:])
            
        
    def height(self):
        height = 1 if (self.__left or self.__right) else 0
        sub_h = 0
        if self.__left:
            sub_h = max(sub_h, self.__left.height())
        
        if self.__right:
            sub_h = max(sub_h, self.__right.height())
        
        height += sub_h
        return height
    
    def __str__(self):
        return str(self.inorder())
    
    def __bool__(self):
        return self.__value is not None
    
    def __eq__(self, other):
        if type(self) == type(other):
            return self.__value == other.__value
        
        elif type(self.__value) == type(other):
            return self.__value == other
        
        return NotImplemented
    
    def __gt__(self, other):
        if type(self) == type(other):
            return self.__value > other.__value
        
        elif type(self.__value) == type(other):
            return self.__value > other
        
        return NotImplemented
    
    def __lt__(self, other):
        if type(self) == type(other):
            return self.__value < other.__value
        
        elif type(self.__value) == type(other):
            return self.__value < other
        
        return NotImplemented
    
if __name__ == "__main__":
    values = list(range(10))
    
    tree = BinaryTree(source=values)
    print(tree)
    
    print(f"preorder: {list(tree.preorder())}")
    
    print(f"inorder: {list(tree.inorder())}")
    
    print(f"postorder: {list(tree.postorder())}")
        
    
