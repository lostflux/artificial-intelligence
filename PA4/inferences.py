#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    This file implements inferencing methods for the backtracking algorithm for CSPs.
"""
__author__ = "Amittai"
__copyright__ = "Copyright 2021"
__credits__ = ["Amittai"]
__email__ = "Amittai.J.Wekesa.24@dartmouth.edu"
__github__ = "@siavava"

from erratum import ( log_error, log_info, log_debug_info )

from Queue import Queue

# from CSP import CSP

def arc_consistency(csp):
    """
        This function implements the Arc Consistency algorithm, AC-3.
    """
    
    # initialize queue of arcs, initially to all arcs
    # (possible pairings of variables).
    queue = Queue()
    for var1 in csp.variables:
        for var2 in csp.variables:
            if var1 != var2:
                queue.add((var1, var2))
    
    # track revisions (we'll potentially need to undo this)
    revisions: set = set()
    
    # fetch all from queue.
    while queue:
        
        # get variable and a next variable from Queue.
        (var, next_var) = queue.remove()
        
        # revise the domain of the variable.
        if revise(csp, var, next_var, revisions):
            
            # get domain
            current_domain = csp.get_domain(var)
            
            # if domain is empty, CSP is not solvable. Return False.
            if not current_domain:
                return None
            
            constraints = [c for c in csp.constraints if var in c and next_var not in c]
            for constraint in constraints:
                var1 = constraint[0]
                var2 = constraint[1]
                if var1 == var:
                    queue.add((var2, var))
                else:
                    queue.add((var1, var))
    
    # if all constraints are satisfied, CSP is solvable. Return True.     
    return revisions

def revise(csp, var, next_var, revisions: set):
    """
        This function implements the revise function for the AC-3 algorithm.
    """
    
    # detect revisions.
    
    # check if the pair of variables is constrained.
    constrained = False
    for constraint in csp.constraints:
        if var in constraint and next_var in constraint:
            constrained = True
            break
        
    # if constrained...
    
    # track revisions
    revised = False
    if constrained:
        
        # check domains.
        current_domain: set = csp.get_domain(var)
        next_domain:set = csp.get_domain(next_var)
        
        # if a value in the current domain would result in the next domain being empty,
        # remove it from the current domain.
        
        to_remove = set()
        for value in current_domain:
            if len(next_domain) == 1 and value in next_domain:
                # current_domain.remove(value)
                to_remove.add(value)
                revisions.add((var, value))
                revised = True
        current_domain -= to_remove
                
    # was a revision / revisions done? pass info back to caller.
    return revised