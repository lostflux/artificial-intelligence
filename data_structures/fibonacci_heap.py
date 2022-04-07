#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    A naive Fibonacci Tree.
"""
__author__ = "Amittai"
__copyright__ = "Copyright 2021"
__credits__ = ["Amittai"]
__email__ = "amittaijoel@outlook.com"
__github__ = "@siavava"

# from linked_list import __FhLinkedList
# from binary_tree import BinaryTree
# from typing import TypedDict

INDEX_ERROR = "Index out of range"
NODE_ERROR = "Node not found."
TYPE_ERROR = "Expected a LinkedList, got different type."

class __FhNode():
    def __init__(self, item, score, next=None, prev=None):
        self.__item = item
        self.__score = score
        self.__size = 1
        self.__children = __FhLinkedList()
        
        # LL mechatronics
        self.prev: __FhNode = prev
        self.next: __FhNode = next
        
    def score(self):
        return self.__score
    
    def size(self):
        return self.__size
        
    def __update_min(self, node):
        assert isinstance(node, __FhNode)
        assert self.__score is not None
        self.__score = min(self.__score, node.__score)
        
    def insert(self, node):
        self.__children.append(node)
        self.__size += node.__size
        self.__update_min(node)
        
    def merge(self, other_node):
        self.insert(other_node)
        return self
        
    @staticmethod
    def merge(node_1, node_2):
        assert isinstance(node_1, __FhNode)\
            and isinstance(node_2, __FhNode)
        if node_1 <= node_2:
            node_1.insert(node_2)
            return node_1
        else:
            node_2.insert(node_1)
            return node_2
        
    def chain(self, node):
        """
            Chains a node into a sequence of nodes.\n
            NOTE: By default, `a.chain(b)` makes `b` the next node of `a`.
            To chain *before*, use `a.chain_before(b)`.
        """
        if self.next:
            node.next = self.next
            node.next.prev = node
        self.next: __FhNode = node
        node.prev = self
    
    def chain_before(self, node):
        if self.prev:
            self.prev.chain(node)
        else:
            self.prev: __FhNode = node
            node.next = self
    
    def unchain(self):
        if self.prev:
            self.prev.next = self.next
        if self.next:
            self.next.prev = self.prev
        
    def advance(self, steps):
        """
            Advances the node by steps 
            NOTE: Assumes that number of advances is valid. Caller should ascertain that!
        """
        node: __FhNode = self
        while node and steps > 0:
            node = node.next
            steps -= 1
        if not node:
            raise ValueError(NODE_ERROR)
        return node
    
    def rewind(self, steps):
        """
            Rewinds the node by steps
            NOTE: Assumes that number of rewinds is valid. Caller should ascertain that!
        """
        node: __FhNode = self
        while node and steps > 0:
            node = node.prev
            steps -= 1
        if not node:
            raise ValueError(NODE_ERROR)
        return node
    
    @staticmethod
    def empty():
        return __FhNode(None)
    
            
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
        return iter(self.__children)
    
class __FhLinkedList:
    """ A naive implementation of a Linked List."""
        
    def __init__(self):
        self.__head = __FhNode.empty()
        self.__tail = __FhNode.empty()
        self.__size = 0

    def __str__(self):
        return str(self.to_list())

    def __repr__(self):
        return repr(self.to_list())

    def __len__(self):
        return self.__size
    
    def __bool__(self):
        return self.__size != 0
    
    
    def to_list(self):
        """
            Generate list version of __FhLinkedList.
        """
        lst = []
        node = self.__head
        while node:
            lst.append(node.value)
            node = node.next
            
        return lst
    
    def append(self, node):
        if not self.__head:
            self.__head = node
            self.__tail = self.__head
        else:
            self.__tail.chain(node)
            self.__tail = self.__tail.next
        self.__size += 1
            
    def __locate(self, index: int):
        """
            Navigate to node at specified index in LL.
            Raises IndexError if index is out of range.
        """
        # /// if valid index, proceed with location ///
        if 0 <= index < self.__size \
            or -self.__size <= index < 0:
            # /// check target against midpoint,
            # /// use path that gives better performance! ///
            target = index if index >= 0 else self.__size + index
            mid = self.__size // 2
            if target <= mid:
                target_node: __FhNode = self.__head.advance(target)
            else:
                steps = (self.__size - (target + 1))
                target_node: __FhNode = self.__tail.rewind(steps)
            return target_node
        # /// invalid index, raise error ///
        raise IndexError(INDEX_ERROR)        

    def __getitem__(self, index):
        """Get item at index"""
        target = self.__locate(index)       # /// throws exception
        return target.value
    
    def pop(self, index=-1):
        """
            Pop item, akin to a Stack operation.
            Removes and returns the item at the given index.
            If no index is specified, a.pop() removes and returns the last item.
            If the stack is empty, INDEX_ERROR is raised.
        """
        target: __FhNode = self.__locate(index)       # /// throws exception
        if not target.prev:
            if target.next:
                self.__head = target.next
            else:
                self.__head = __FhNode.empty()
        if not target.next:
            if target.prev:
                self.__tail = target.prev
            else:
                self.__tail = self.__head

        target.unchain()
        self.__size -= 1
        return target
        
    def reverse(self):
        """ Reverse *IN PLACE* """
        # /// BACKTRACK 
        # ///   SWAP PREDECESSOR,-SUCCESSOR ///
        rev = None
        forw = self.__head
        rev_head = None
        while forw:
            rev = __FhNode(forw.value, prev=rev)
            if not rev.prev: rev_head = rev
            elif rev.prev: rev.prev.next = rev
            forw = forw.next
        self.__head, self.__tail = rev_head, rev
        
    # /// QUEUE methofs ///
    """ Enqueue and Dequeue are the same as push and pop """
    def enqueue(self, obj):
        """ Enqueue item; akin to a Queue operation"""
        self.append(obj)
        
    def dequeue(self):
        """ Dequeue item; akin to a Queue operation"""
        return self.pop(0)
    
    def push(self, item):
        """ Push item; akin to a Stack operation"""
        self.append(item)
        
    def remove(self, node):
        assert isinstance(node, __FhNode)
        node.unchain()

    def __setitem__(self, index, value):
        target = self.__locate(index)       # /// throws exception
        target.item = value

    def __delitem__(self, index):
        target: __FhNode = self.__locate(index)       # /// throws exception
        if index == 0: 
            self.__head = target.next
        elif index == 1: 
            self.tail = target.prev
        target.unchain()
        del target
        self.__size -= 1

    def __contains__(self, item):
        current = self.head
        while current:
            if current.item == item:
                return True
            current = current.next
        return False

    def __iter__(self):
        current = self.__head
        while current:
            yield current
            current = current.next

    def __reversed__(self):
        current = self.__tail
        while current:
            yield current.value
            current = current.prev
            
    def merge(self, other):
        """ Merge two LinkedLists """
        if not isinstance(other, __FhLinkedList):
            raise TypeError(TYPE_ERROR)
        self.__tail.chain(other.__head)
        self.__tail = other.__tail
        self.__size += other.__size
    
class FibonacciHeap(object):
    """
        A Fibonacci Heap implementation.
    """
    def __init__(self):
        self.__nodes = __FhLinkedList()
        self.__min = None
        self.__size = 0
        
    def size(self):
        return self.__size

    def insert(self, item, score):
        """
            Insert a key into the Fibonacci Heap.
        """
        node = __FhNode(item, score)
        self.__size += 1
        self.update_min(node)
        self.__nodes.append(node)
                
    def update_min(self, node):
        if self.__min is None: 
            self.__min: __FhNode = node
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
            assert isinstance(node, __FhNode)
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
                    node_1: __FhNode = sizes[size].pop()
                    node_2: __FhNode = sizes[size].pop()
                    self.__nodes.remove(node_1)
                    self.__nodes.remove(node_2)
                    
                    merged = __FhNode.merge(node_1, node_2)
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
