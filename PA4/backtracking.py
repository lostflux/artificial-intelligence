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

from numpy import log
from CSP import CSP
from erratum import ( log_error, log_info, log_debug_info )


def backtracking_search(csp: CSP):
    """
        Backtracking search algorithm.
        Returns the first solution found.
    """
    return backtrack({}, csp)

def backtrack(assignments: dict, csp: CSP):
    
    if csp.is_completed(assignments):
        return assignments
    
    variable = csp.get_unassigned_variable(assignments)
    
    for value in csp.order_values(variable, assignments):
        
        if csp.is_consistent(assignments, variable, value):
            
            assignments[variable] = value
            
            if csp.debug: log_debug_info(assignments)
            
            result = backtrack(assignments, csp)
            
            if result: return result
            
            del assignments[variable]
        
    return None