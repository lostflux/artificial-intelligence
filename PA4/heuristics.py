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

from numpy import inf                                       # infinity

# from CSP import CSP                                       #! Muted because it causes circular import.

###############################################################################
#################### Functionality for the MRV heuristic ######################
###############################################################################

def mrv_heuristic(csp, unassigned: list, deg_heuristic: bool):
    """
        This function implements the MRV (Minimum Remaining Values) heuristic.
        It returns the variable with the fewest legal values.
    """
    
    # track the variable with least remaining values 
    least_var, least_count = None, inf
    
    # track variables with the same least remaining values
    # this is helpful when using degree heuristic as a tie-breaker.
    tied_vars: list = []
    
    # loop over unassigned variables
    for var in unassigned:
        
        # check the size of the domain for the variable.
        count = len(csp.get_domain(var))
        
        # if size is greater than least size, remember the current variable.
        if count < least_count:
            least_count = count
            least_var = var
            
            # if degree heuristic is used, 
            # clear the list of tied variables.
            # and add the current variable to the list.
            if deg_heuristic: tied_vars = [var]
            
        # if size is equal to least size,
        # append variable to list of tied variables.
        elif count == least_count and degree_heuristic:
            tied_vars.append(var)
    
    # if degree heuristic is used,
    # return the variable with the most constraints.
    if deg_heuristic:
        return degree_heuristic(csp, tied_vars)
        
    # return the variable with the least number of remaining values.
    return least_var
    
###############################################################################
################## Functionality for the Degree heuristic #####################
###############################################################################
    
def degree_heuristic(csp, unassigned):
    """
        This function implements the Degree heuristic.
        It returns the variable with the most contraints on other variables.
    """
    
    # map each variable to the degree of constraints on other variables.
    degrees: dict = {}
    for constraint in csp.constraints:
        for var in constraint:
            degrees[var] = degrees.get(var, 0) + 1
    
    # track maximum degree, variable
    max_var, max_degree = None, -inf
    
    # iterate over every unassigned variable
    # if variable has higher degree, remember it.
    for var in unassigned:
        degree = degrees.get(var, 0)
        if degree > max_degree:
            max_degree = degree
            max_var = var
    
    # remember variable with highest degree
    return max_var
    
###############################################################################
#################### Functionality for the LCV heuristic ######################
###############################################################################

def lcv_heuristic(csp, var, unassigned_vars):
    """
        This function implements the LCV (Least Constraining Value) heuristic.
        NOTE: Unlike with the others, this selects a list of `value`s and not a `variable`.
    """
    
    # get domain for current varible
    domain = csp.get_domain(var)
    
    # if domain is singular, return the singular value.
    if len(domain) == 1: return list(domain)
    
    # initialize restrictions
    restrictions: dict = {}
    
    # check all constraints in the CSP.
    for constraint in csp.constraints:
        
        # if a constraint contains a specified variable;
        # check which values the two variables have in common
        # and increment their restriction in the dictionary.
        # NOTE: we only do this for unassigned variables.
        if var in constraint:
            other_var = constraint[0] if var != constraint[0] else constraint[1]
            if other_var in unassigned_vars:
            
                # get respective domains.
                vars1: set = csp.get_domain(var)
                vars2: set = csp.get_domain(other_var)
                
                # get intersection (values in common)
                intersection: set = vars1 & vars2
                
                # increment restriction for values in common.
                for val in intersection:
                    restrictions[val] = restrictions.get(val, 0) + 1
                    
    # return the domain rearranged by the given restrictions.
    sorted_values = sorted(list(domain), key=lambda x: restrictions.get(x, 0))
    
    # return list of sorted values.
    return sorted_values