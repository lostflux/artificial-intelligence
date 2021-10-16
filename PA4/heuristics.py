#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    This file implements a generalized handler for CSPs (Constraint Satisfaction Problems).
"""
__author__ = "Amittai"
__copyright__ = "Copyright 2021"
__credits__ = ["Amittai"]
__email__ = "Amittai.J.Wekesa.24@dartmouth.edu"
__github__ = "@siavava"

from erratum import ( log_error, log_info, log_debug_info )

from numpy import inf                                       # infinity

from PriorityQueue import PriorityQueue

# from CSP import CSP

heuristics_list = ["degree_heuristic", "lcv_heuristic", "mrv_heuristic"]


###############################################################################
#################### Functionality for the MRV heuristic ######################
###############################################################################

def mrv_heuristic(csp, unassigned: list):
    """
        This function implements the MRV heuristic.
        It returns the variable with the fewest legal values.
    """
    
    least_var, least_count = None, inf
    
    for var in unassigned:
        
        count = len(csp.get_domain(var))
        
        if count < least_count:
            least_count = count
            least_var = var
        
    return least_var
    
###############################################################################
################## Functionality for the Degree heuristic #####################
###############################################################################
    
def degree_heuristic(csp):
    """
        This function implements the Degree heuristic.
        It returns the variable with the most contraints on other variables.
    """
    
    degrees: dict = {}
    
    for constraint in csp.constraints:
        for var in constraint:
            degrees[var] = degrees.get(var, 0) + 1
    
    min_var, min_degree = None, -inf
    
    for var in csp.get_unassigned_variables():
        degree = degrees.get(var, 0)
        
        if degree > min_degree:
            min_degree = degree
            min_var = var
        
    return min_var
    
###############################################################################
#################### Functionality for the LCV heuristic ######################
###############################################################################

def lcv_heuristic(csp, var, unassigned_vars, debug=False):
    
    domain = csp.get_domain(var)
    
    if len(domain) == 1: return list(domain)
    
    restrictions: dict = {}
    
    for constraint in csp.constraints:
        
        if var in constraint:
        
            other_var = constraint[0] if var != constraint[0] else constraint[1]
            
            if other_var in unassigned_vars:
            
                vars1: set = csp.get_domain(var)
                vars2: set = csp.get_domain(other_var)
                
                intersection: set = vars1 & vars2
                
                for val in intersection:
                    restrictions[val] = restrictions.get(val, 0) + 1
    sorted_values = sorted(list(domain), key=lambda x: restrictions.get(x, 0))
    
    return sorted_values