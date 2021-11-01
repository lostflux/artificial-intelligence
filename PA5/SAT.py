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


import sys
import random
from numpy import ( inf ) 
from Sudoku import Sudoku
from TwoWayDict import TwoWayDict

from erratum import (log_error, log_info, log_debug_info)

class SAT:
    def __init__(self, filename, max_iterations=2000, threshold=0.1):
        
        self.clauses = set()
        self.assignments = []
        self.mappings = TwoWayDict()  # NOTE: key = variable, value = index of that variable in the assignment list
        self.threshold = threshold
        self.max_iterations = max_iterations
        
        try:
            self.sudoku = Sudoku()
            # self.sudoku.load(filename)
            self.initialize(filename)
        except IOError as err:
            log_error(err)
            sys.exit()
    
    
    def initialize(self, filename):
        try:
            with open(filename, 'r') as f:
                pos = 0
                self.assignments.append(0)  
                for line in f:
                    line = str(line)
                    self.clauses.add(line)
                    
                    items = line.replace('-', '').split()
                    
                    for item in items:
                        variable = str(item)
                        
                        if variable not in self.mappings:
                            self.mappings.add(variable, pos)
                            # self.assignments.append(0)   
                            pos += 1
                f.close()
        except IOError as err:
            raise IOError(err)
        
        self.assignments = [0] * len(self.mappings)
        
        # log_info(str(self.mappings))
        
    def random_assign(self):
        for index in range(len(self.assignments)):
            self.assignments[index] = random.randint(0, 1)
            
            
    def satisfied_clauses(self):
        
        count = 0
        for clause in self.clauses:
            
            clause_elements = clause.split()
            
            for clause_element in clause_elements:
                
                var = str(clause_element)
                
                # if constraint is negative and assignment is 0, then satisfied
                if var[0] == '-':
                    # trim the '-'
                    var = var[1:]
                    index = self.mappings[var]
                    if not self.assignments[index]:
                        count += 1 
                        break
                    
                # if constraint is positive and assignment is 1, then satisfied
                elif self.assignments[self.mappings[var]]:
                    # else, if assigned, return True
                    count += 1
                    break
                
            # return all satisfied clauses
        return count
        
    
    def random_max(self):
        max_index = 0
        max_value = 0
        for index in range(len(self.assignments)):
            if self.assignments[index] > max_value:
                max_index = index
                max_value = self.assignments[index]
        return max_index
    
    def highest_vars(self):
        highest = -inf
        
        _vars = set()
        for index in range(len(self.assignments)):
            
            self.assignments[index] = 1 - self.assignments[index]
            score = self.satisfied_clauses()
            if score >= highest:
                highest = score
                if score > highest:
                    _vars = set()
                _vars.add(index)
            self.assignments[index] = 1 - self.assignments[index]
                
        return list(_vars)

    def gsat(self):
        
        self.random_assign()
        
        iteration = 0 
        while iteration < self.max_iterations:
            
            
            log_debug_info(f"Iterations: {iteration}, satisfied = {self.satisfied_clauses()} out of {len(self.clauses)}")
                
            # if all clauses are satisfied, return True
            if self.satisfied_clauses() == len(self.clauses):
                return self.assignments
            
            # generate a random probability
            probability = random.random()
            
            # if above threshold, flip random variable
            if probability < self.threshold:
                index = random.randint(1, len(self.assignments))
                self.assignments[index-1] = not self.assignments[index-1]
                
            # if below variable, pick variable with max value 
            else:
                highest_indices = self.highest_vars()
                
                index = random.choice(highest_indices)
                
                self.assignments[index] = not self.assignments[index]
            
            # increment trials
            iteration += 1
            
        # if no result found, return False
        return False
    
    def walksat(self):
        
        iteration = 0
        self.random_assign()
        
        while iteration < self.max_iterations:
            pass
            
        
        
    
    def write_solution(self, filename):
        try:
            with open(filename, "w") as f:

                # iterate through variables
                for index in range(len(self.assignments)):
                    var = ""

                    # if variable is negated, add a '-' sign
                    if not self.assignments[index]:
                        var += "-"

                    # add corresponding clause variable (string), and newline
                    var += self.mappings.get_key(index) #[index]
                    var += "\n"

                    f.write(var)

                f.close()
            
        except IOError:
            log_error("Error: File not found")
    
    
        