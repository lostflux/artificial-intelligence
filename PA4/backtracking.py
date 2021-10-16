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
from erratum import ( log_error, log_info, log_debug_info )


def backtracking_search(csp, variable_heuristic=None, value_heuristic=None, inference=None):
    """
        Backtracking search algorithm.
        Returns the first solution found.
    """
    return backtrack({}, csp)

def backtrack(assignments: dict, csp: CSP):
    
    if csp.is_completed(assignments):
        return assignments
    
    for variable in csp.select_unassigned_variables(assignments):
    
        for value in csp.order_values(variable, assignments):
            
            if csp.is_consistent(assignments, variable, value):
                
                assignments[variable] = value
                
                if csp.debug: log_debug_info(assignments)
                
                result = backtrack(assignments, csp)
                
                if result: return result
                
                del assignments[variable]
        
    return None