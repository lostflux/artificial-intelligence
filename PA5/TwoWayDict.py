#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    This file implements a 2-way dictionary.
    
"""
__author__ = "Amittai"
__copyright__ = "Copyright 2021"
__credits__ = ["Amittai"]
__email__ = "Amittai.J.Wekesa.24@dartmouth.edu"
__github__ = "@siavava"



class TwoWayDict(dict):
    """
        A 2-way dictionary.
    """
    
    def __init__(self, *args, **kwargs):
        """
            Initialize the 2-way dictionary.
        """
        self.__keys = dict()        # mapping of keys to values.
        self.__values = dict()      # reverse mapping of values to keys.
            
    def add(self, key, value):
        """
            Add key - value pair to the 2-way dictionary.
        """        
        self.__keys[key] = value
        self.__values[value] = key
        
    def __setitem__(self, key, value):
        self.__keys[key] = value
        self.__values[value] = key
        
    def __getitem__(self, key):
        """
            Get the value associated with the given key.
        """
        return self.__keys[key]
    
    def get_key(self, value):
        """
            Get the key associated with the given value.
        """
        return self.__values[value]
    
    def get_value(self, key):
        """
            Get the value associated with the given key.
        """
        return self.__keys[key]
    
    def delete_key(self, key):
        """
            Delete a binding by key.
        """
        if key in self.__keys:
            value = self.__keys[key]
            del self.__keys[key]
            del self.__values[value]
            
    def delete_value(self, value):
        
        if value in self.__values:
            key = self.__values[value]
            del self.__values[value]
            del self.__keys[key]
    
    def __str__(self):
        return "key -> val " + str(self.__keys) + "\n" + "val -> key " + str(self.__values)
    
    def __len__(self):
        return len(self.__keys)
    
    def __contains__(self, key):
        return key in self.__keys
    
    def contains_value(self, value):
        return value in self.__values
