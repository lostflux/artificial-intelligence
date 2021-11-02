#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    This file implements a generalized handler for Boolean Satisfiability Problems.
    Although we test it on Sudoku, the handler should be able to solve any type of problem
    and not just Sudoku.
"""
__author__ = "Amittai"
__copyright__ = "Copyright 2021"
__credits__ = ["Amittai"]
__email__ = "Amittai.J.Wekesa.24@dartmouth.edu"
__github__ = "@siavava"


import sys
import random
from numpy import ( inf )
from TwoWayDict import TwoWayDict

from erratum import (log_error, log_info, log_debug_info)

class SAT:
    """
        A generic solver for Binary Logic Satisfiability problems.
    """
    def __init__(self, filename, max_iterations=100000, threshold=0.3):
        
        # initialize parameters
        self.clauses = set()                    # set of all clauses
        self.assignments = []                   # list of assignments
        self.mappings = TwoWayDict()            # NOTE: key = clause, value = index of clause in assignment list
        self.threshold = threshold              # threshold probability of choosing randomly.
        self.max_iterations = max_iterations    # maximum number of iterations
        
        # load clauses from the file and initialize the SAT.
        # If file IO fails, exit immediately.
        self.initialize(filename)
    
    
    def initialize(self, filename):
        """
            Load clauses from file and save them.
            Caller should handle File IO exceptions.
        """
        with open(filename, 'r') as f:
            index = 0 
            
            # Loop over lines, saving every unique clause.
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
            
        # initialize an assignment of "0" to every clause.
        self.assignments = [0] * index
        
    def random_assign(self):
        """
            Randomly assign 1's to *some* clauses.
        """
        for index in range(len(self.assignments)):
            self.assignments[index] = random.randint(0, 1)
            
            
    def satisfied_clauses(self, walksat=False):
        """
            Count the number of satisfied clauses in the current assignment.
        """
        
        # if using walksat, 
        # track a set of plausible candidates for next flips.
        if walksat:
            self.walksat_candidates = set()
        
        # For each clause in the SAT,
        # Check its constituent components -- if satisfied, increment count.
        count = 0
        for clause in self.clauses:
            
            clause_elements = clause.split()
            
            if walksat: clause_satisfied = False        # if using walksat, track whether the current clause has been satisfied.
            
            # for each clause element...
            # check if satisfied.
            for clause_element in clause_elements:
                
                var = str(clause_element)
                
                # if negative constraint is NOT assigned, then satisfied
                if var[0] == '-':
                    # trim the '-'
                    var = var[1:]
                    index = self.mappings[var]
                    if not self.assignments[index]:
                        count += 1 
                        clause_satisfied = True
                        break
                    
                # if positive constraint is assigned, then satisfied
                elif self.assignments[self.mappings[var]]:
                    # else, if assigned, return True
                    count += 1
                    clause_satisfied = True
                    break
            
            # if using walksat and all elements in the clause not satisfied,
            # add to candidates for the next flip.
            if walksat and not clause_satisfied:
                self.walksat_candidates.add(clause)
                
        # return count of all satisfied clauses
        return count
    
    def gsat_highest_vars(self):
        """
            Get the clauses which yield the best satisfaction rate when flipped.
        """
        
        # iterate over each clause, flip it,
        # and check the satisfiability of the ecosystem.
        highest = -inf
        
        _vars = set()
        for index in range(len(self.assignments)):
            
            self.assignments[index] = not self.assignments[index]
            score = self.satisfied_clauses()
            if score >= highest:
                highest = score
                if score > highest:
                    _vars = set()
                _vars.add(index)
            self.assignments[index] = not self.assignments[index]
                
        return random.choice(list(_vars))
    
    def walksat_highest_variable(self, clause):
        """
            Get the single highest variable for WalkSAT.
            This differs from the procedure for GSAT in that 
            we check through the pre-selected candidates only
            instead of looping through all the clauses.
        """
        
        # iterate through all candidates, building a set of highest scorers.
        highest = -inf
        highest_variables = set()
        variables = clause.split()
        
        for variable in variables:
            variable = variable.replace('-', '')
            index = self.mappings[variable]
            self.assignments[index] = not self.assignments[index]
            score = self.satisfied_clauses()
            if score >= highest:
                
                # if new high score, reset the set of saved variables.
                if score > highest:
                    highest_variables = set()
                    highest = score
                highest_variables.add(variable)
                
            self.assignments[index] = not self.assignments[index]
    
        # Choose a random variable from the set of surviving candidates.
        variable = random.choice(list(highest_variables))
                
        # return the ndex of that one variable.
        return self.mappings[variable]

    def gsat(self):
        """
            GSAT Algorithm for Binary Logic Satisfiability.
        """
        
        # Start with a random assignment.
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
                self.assignments[index] = not self.assignments[index]
                
            # if below threshold, pick variable with max value 
            else:
                index = self.gsat_highest_vars()
                
            # flip the assignment.
            self.assignments[index] = not self.assignments[index]
            
            # increment trials
            iteration += 1
            
        # if no result found, return False
        return False
    
    def walksat(self):
        """
            WalkSAT algorithm for Binary Logic Satisfiability.
        """
        
        # Start with a random assignment.
        #   Why? I sort of got better performance out of WalkSAT
        #   let it start with the default assignment of all ZEROs.
        self.random_assign()
        
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
            
            # if below threshold, choose random variable in clause
            if probability < self.threshold:
                
                variable = random.choice(clause.split()).replace('-', '')
                
                index = self.mappings[variable]
                
            # if above threshold, pick variable with max value 
            else:
                
                index  = self.walksat_highest_variable(clause)\
                
            
            # increment iterations and flip the variable.
            iteration += 1
            self.assignments[index] = not self.assignments[index]
            
            
        # if no result found, return False
        return False
        
    
    def write_solution(self, filename):
        """
            Write a SAT solution into a file.
            
        """
        with open(filename, "w") as f:

            # iterate through variables
            for index in range(len(self.assignments)):
                var = ""

                # if variable is negated, add a '-' sign
                if not self.assignments[index]:
                    var += "-"

                # add corresponding clause variable (string), and newline
                var += self.mappings.get_key(index)
                var += "\n"

                f.write(var)

            f.close() 
    
        