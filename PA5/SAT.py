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
    def __init__(self, filename, max_iterations=100000, threshold=0.3):
        
        self.clauses = set()
        self.assignments = []
        self.mappings = TwoWayDict()  # NOTE: key = variable, value = index of that variable in the assignment list
        self.threshold = threshold
        self.max_iterations = max_iterations
        
        try:
            self.initialize(filename)
        except IOError as err:
            log_error(err)
            sys.exit()
    
    
    def initialize(self, filename):
        with open(filename, 'r') as f:
            index = 0
            self.assignments.append(0)  
            for line in f:
                line = str(line)
                self.clauses.add(line)
                
                items = line.replace('-', '').split()
                
                for item in items:
                    variable = str(item)
                    
                    if variable not in self.mappings:
                        self.mappings[variable] = index
                        index += 1
            f.close()
    
        self.assignments = [0] * index
        
    def random_assign(self):
        for index in range(len(self.assignments)):
            self.assignments[index] = random.randint(0, 1)
            
            
    def satisfied_clauses(self, walksat=False):
        
        if walksat:
            self.walksat_candidates = set()
        
        count = 0
        for clause in self.clauses:
            
            clause_elements = clause.split()
            
            if walksat: clause_satisfied = False
            
            for clause_element in clause_elements:
                
                var = str(clause_element)
                
                # if constraint is negative and assignment is 0, then satisfied
                if var[0] == '-':
                    # trim the '-'
                    var = var[1:]
                    index = self.mappings[var]
                    if not self.assignments[index]:
                        count += 1 
                        clause_satisfied = True
                        break
                    
                # if constraint is positive and assignment is 1, then satisfied
                elif self.assignments[self.mappings[var]]:
                    # else, if assigned, return True
                    count += 1
                    clause_satisfied = True
                    break
            
            if walksat and not clause_satisfied:
                self.walksat_candidates.add(clause)
                
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
    
    def gsat_highest_vars(self):
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
                
        return random.choice(list(_vars))
    
    def walksat_highest_variable(self, clause):
        highest = -inf
        
        highest_variables = set()
        
        variables = clause.split()
        
        for variable in variables:
            variable = variable.replace('-', '')
            
            index = self.mappings[variable]
            
            self.assignments[index] = not self.assignments[index]
            score = self.satisfied_clauses()
            if score >= highest:
                
                if score > highest:
                    highest_variables = set()
                highest = score
                highest_variables.add(variable)
                
            self.assignments[index] = not self.assignments[index]
    
        variable = random.choice(list(highest_variables))
                
        return self.mappings[variable]

    def gsat(self):
        
        self.random_assign()
        
        iteration = 0 
        while iteration < self.max_iterations:
            
            
                
            # if all clauses are satisfied, return True
            satisfied_clauses = self.satisfied_clauses()
            log_debug_info(f"Iterations: {iteration}, satisfied = {satisfied_clauses} out of {len(self.clauses)}")
            
            if satisfied_clauses == len(self.clauses):
                return self.assignments
            
            
            # generate a random probability
            probability = random.random()
            
            # if above threshold, flip random variable
            if probability < self.threshold:
                
                index = random.randint(0, len(self.assignments)-1)
                self.assignments[index-1] = not self.assignments[index-1]
                
            # if below variable, pick variable with max value 
            else:
                index = self.gsat_highest_vars()
                
            self.assignments[index] = not self.assignments[index]
            
            # increment trials
            iteration += 1
            
        # if no result found, return False
        return False
    
    def walksat(self):
        
        # self.random_assign()
        
        iteration = 0 
        while iteration < self.max_iterations:
                
            # if all clauses are satisfied, return True
            satisfied_clauses = self.satisfied_clauses(walksat=True)
            log_debug_info(f"Iterations: {iteration}, satisfied = {satisfied_clauses}, out of {len(self.clauses)}")
           
            if satisfied_clauses == len(self.clauses):
                return self.assignments
            
            
            # get random clause from candidates
            clause = random.choice(list(self.walksat_candidates))
            
            # generate a random probability
            probability = random.random()
            
            # if above threshold, flip random variable in clause
            if probability < self.threshold:
                
                variable = random.choice(clause.split()).replace('-', '')
                
                index = self.mappings[variable]
                
            # if below threshold, pick variable with max value 
            else:
                
                index  = self.walksat_highest_variable(clause)\
                
            
            # increment trials
            iteration += 1
            self.assignments[index] = not self.assignments[index]
            
            
        # if no result found, return False
        return False
        
    
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
    
    
        