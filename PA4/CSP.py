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

import heuristics

# from heuristicsmrv_heuristic, degree_heuristic, lcv_heuristic )

class CSP():
    
    def __init__(self, variables=None, domains=None, constraints=None, mrv=False, \
        degree_heuristic=False, lcv=False, inference=False, debug=False):
        """
            Constructor for the Constrained Search Problem.
            :arg variables: A `set` of variables in the CSP.
            :arg domains: A `disctionary` of variables -> domains in the CSP.
            :arg constraints: A set of constraints in the CSP.
        """
        
        # initialize varibles
        self.variables: set = variables if variables else set()
        self.domains: dict = domains if domains else {}
        self.constraints: set = constraints if constraints else set()
        self.needed_assignments: int = len(variables) if variables else 0
        self.solution = None
        
        # enable or disable heuristics
        self.mrv = mrv
        self.degree_heuristic = degree_heuristic
        self.lcv = lcv
        
        # enable or disable debug mode
        self.debug = debug
        
        
    def __str__(self):
        return f"\n...\nCSP\n\tvariables: \t{self.variables} \
                    \n\tdomains : \t{self.domains} \
                    \n\tconstraints : \t{self.constraints} \
                    \n\tsolution:\t{self.solution} \
                    \n...\n"
        
    def add_variable(self, var, domain):
        """
            Add a new variable into the CSP.
        """
        self.variables.add(var)
        self.domains[var] = domain
        self.needed_assignments += 1
        
    def add_constraint(self, var1, var2):
        self.constraints.add((var1, var2))

    def get_domain(self, var):
        """Returns the domain for the given variable."""
        return self.domains[var]
    
    def order_values(self, var, assignment):
        if not self.lcv:
            return self.domains[var]
        
        unassigned_vars = [var for var in self.variables if var not in assignment]
        
        return heuristics.lcv_heuristic(self, var, unassigned_vars)

    def get_values_for_constraint(self, var1, var2):
        domain1: set = self.domains[var1]
        domain2: set = self.domains[var2]
        return domain1 ^ domain2
    
    def get_unassigned_variable(self, assignment):
        
        if not self.mrv:
            for var in self.variables:
                if var not in assignment:
                    return var
            return None
        
        else:
            unassigned = [var for var in self.variables if var not in assignment]
            return heuristics.mrv_heuristic(self, unassigned)
    

    def satisfies_constraint(self, constraint: tuple, assignments: dict, variable, value):
        if len(constraint) != 2:
            log_error(f"Invalid constraint dimension: {constraint}")
            return False
        
        other_variable = constraint[0] if constraint[0] != variable else constraint[1]
        
        if other_variable not in assignments:
            return True
        
        return assignments[other_variable] != value

    def is_consistent(self, assignments: dict, variable, value):
        
        for constraint in self.constraints:
            if variable not in constraint:
                continue
            elif not self.satisfies_constraint(constraint, assignments, variable, value):
                return False
        return True
    
    def is_completed(self, assignments: dict):
        complete = len(assignments) == self.needed_assignments
        if complete:
            self.solution = assignments
            
        return complete