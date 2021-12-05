#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    This file implements the backtracking algorithm for CSPs.
"""
__author__ = "Amittai"
__copyright__ = "Copyright 2021"
__credits__ = ["Amittai"]
__email__ = "Amittai.J.Wekesa.24@dartmouth.edu"
__github__ = "@siavava"

from CSP import CSP
from inferences import arc_consistency as inference     # import the inference function

def backtracking_search(csp: CSP, inferencing=False):
    """
        Backtracking search algorithm.
        Returns the first solution found.
    """
    return backtrack({}, csp, inferencing)

def backtrack(assignments: dict, csp: CSP, inferencing: bool):
    """
        Recursively search and backtrack until a solution is found
        or we determine that the CSP is unsolvable.
    """
    
    # if assignments complete, return the assignments.
    if csp.is_completed(assignments):
        return assignments
    
    # get an unassigned variable.
    variable = csp.get_unassigned_variable(assignments)
    
    # just to avoid likely errors, declare a revisions set
    revisions = set()
    
    # try out every possible value for the variable.
    for value in csp.order_values(variable, assignments):
        
        # if assignment is consistent
        if csp.is_consistent(assignments, variable, value):
            
            # save the assignment
            assignments[variable] = value
            
            # extra step: revise the domains of the CSP.
            if inferencing: revisions: set = inference(csp)
                
            # recursively search for a solution.
            result = backtrack(assignments, csp, inferencing)
                
            # return the result if one was found.
            if result: return result
                
            # if no result found, undo the revisions
            # and delete the assignment.
            if inferencing: undo_revisions(csp, revisions)
            del assignments[variable]
        
    # return no solution
    return None

def undo_revisions(csp: CSP, revisions: set):
    """
        Function to undo domain revisions
    """
    
    # iterate over all revisions;
    #   reinstate the values in the domains of the respective variables.
    for (variable, value) in revisions:
        csp.get_domain(variable).add(value)
        