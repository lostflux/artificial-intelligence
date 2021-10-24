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

# from heuristics import ( mrv_heuristic, degree_heuristic, lcv_heuristic )  # muted import due to circular dependency

class CSP():
    
    def __init__(self, variables=None, domains=None, constraints=None, mrv=False, \
                    lcv=False, degree=False, debug=False):
        """
            Constructor for the Constrained Search Problem.
            :arg variables: A `set` of variables in the CSP.
            :arg domains: A `disctionary` of variables -> domains in the CSP.
            :arg constraints: A set of constraints in the CSP.
        """
        
        self.variable_mappings = dict()
        self.value_mappings = []
        self.variables = set()
        self.domains: list = []
        self.constraints = set()
        
        # initialize variables
        self.initialize(variables, domains, constraints)
        
        # initialize varibles
        self.needed_assignments: int = len(variables) if variables else 0
        self.solution = None
        
        # enable or disable heuristics
        self.mrv = mrv
        self.degree = degree
        self.lcv = lcv
        
        
        # enable or disable debug mode
        self.debug = debug
        
    def initialize(self, variables, domains, constraints):
        """
            Sets up the variables in the CSP.
        """
        for var in variables:
            num_var = len(self.variables)
            self.variables.add(num_var)
            self.variable_mappings[num_var] = var
            
            self.domains.append(set())
            domain = domains.get(var)
            if domain:
                for value in domain:
                    if not value in self.value_mappings:
                        self.value_mappings.append(value)
                        
                    val_index = self.value_mappings.index(value)
                    self.domains[-1].add(val_index)
            
        for constraint in constraints:
            var1 = [key for key, value in self.variable_mappings.items() if value == constraint[0]][0]
            var2 = [key for key, value in self.variable_mappings.items() if value == constraint[1]][0]
            self.constraints.add((var1, var2))
            
        
    def display(self, assignments=None):
        """
            Displays the current state of the CSP.
        """
        
        self.solution = dict()
        
        if assignments:
            for key, value in assignments.items():
                self.solution[self.variable_mappings.get(key, "null")] = self.value_mappings[value]
            
        log_info(self)
        
        
    def __str__(self):
        
        string = ""
        if self.debug: 
            string += f"\tVariables: {self.variables}\n"
            string += f"\tDomains: {self.domains}\n"
            string += f"\tConstraints: {self.constraints}\n"
            string += f"\tVariable mappings: {self.variable_mappings}\n"
            string += f"\tValue mappings: {self.value_mappings}\n"
        
        string += f"\n...\nCSP\n\tvariables: \t{self.variables} \
                    \n\tdomains : \t{self.domains} \
                    \n\tconstraints : \t{self.constraints} \
                    \n\tsolution:\t{self.solution} \
                    \n...\n"
                    
        if self.debug:
            string += f"\n\n\tHeuristics enabled:\n"
            string += f"\t\tMRV: {self.mrv}\n"
            string += f"\t\tDegree: {self.degree}\n"
            string += f"\t\tLCV: {self.lcv}\n"
                    
        return string
        
    def add_variable(self, var, domain):
        """
            Add a new variable into the CSP.
        """
        self.variables.add(var)
        self.domains[var] = domain
        self.needed_assignments += 1
        
    def add_constraint(self, var1, var2):
        """
            Add a new constraint between two variables.
        """
        self.constraints.add((var1, var2))

    def get_domain(self, var) -> set:
        """Returns the domain for the given variable."""
        return self.domains[var]
    
    def remove_value(self, var, value):
        """
            Removes value from the domain of the specified variable.
        """
        self.domains[var].remove(value)
    
    def order_values(self, var, assignments):
        """
            Orders the values in the domain of the specified variable.
        """
        if not self.lcv:
            return self.domains[var]
        
        unassigned_vars = [var for var in self.variables if var not in assignments]
        
        if self.debug: log_error(f"Unassigned variables: {unassigned_vars}")
        
        return heuristics.lcv_heuristic(self, var, unassigned_vars)

    def get_values_for_constraint(self, var1, var2):
        """
            Returns the values common to two variables in a constraint.
        """
        domain1: set = self.domains[var1]
        domain2: set = self.domains[var2]
        return domain1 ^ domain2
    
    def get_unassigned_variable(self, assignments):
        """
            Returns an unassigned variable in the CSP.
        """
        
        if not self.mrv:
            if self.degree:
                unassigned = [var for var in self.variables if var not in assignments]
                return heuristics.degree_heuristic(self, unassigned)
            else:
                for var in self.variables:
                    if var not in assignments:
                        return var
                return None
        
        else:
            unassigned = [var for var in self.variables if var not in assignments]
            return heuristics.mrv_heuristic(self, unassigned, self.degree)

    def satisfies_constraint(self, constraint: tuple, assignments: dict, variable, value):
        """
            Checks if the given value satisfies the constraint, given prior assignments.
        """
        if len(constraint) != 2:
            log_error(f"Invalid constraint dimension: {constraint}")
            return False
        
        other_variable = constraint[0] if constraint[0] != variable else constraint[1]
        
        if other_variable not in assignments:
            return True
        
        return assignments[other_variable] != value

    def is_consistent(self, assignments: dict, variable, value):
        """
            Checks if the given value is consistent with the CSP,
            i.e. it satisfies ALL constraints in the CSP,
            given prior assignments.
        """
        
        for constraint in self.constraints:
            if variable not in constraint:
                continue
            elif not self.satisfies_constraint(constraint, assignments, variable, value):
                return False
        return True
    
    def is_completed(self, assignments: dict):
        """
            Returns true if and only if all variables in the CSP have a consistent assignment.
        """
        
        return len(assignments) == self.needed_assignments
    
    def renders_unsolvable(self, var, value, other_var):
        """
            Returns true if and only if the given value, 
            despite being consistent with the prior assignments,
            renders the CSP unsolvable because it takes away a single
            remaining option for assignment to another unassigned variable.
        """
        next_domain = self.domains[other_var]
        return (len(next_domain) == 1) and (value in next_domain)
    
if __name__ == '__main__':
   
   
    # Create a CSP
    
    variables: set = {"Amittai", "Alphonso", "Fabricio"}
    domains: dict = {"Alphonso": {1, 2, 3}, "Amittai": {1},  "Fabricio": {1, 2}}
    constraints: set = { ("Amittai", "Alphonso"), ("Amittai", "Fabricio"), ("Alphonso", "Fabricio")}
    
    csp = CSP(variables=variables, domains=domains, constraints=constraints, mrv=True, lcv=True, debug=True)
    
    csp.display()
    