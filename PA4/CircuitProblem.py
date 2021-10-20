#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    This file implements test routines for CSP algorithms.
"""
__author__ = "Amittai"
__copyright__ = "Copyright 2021"
__credits__ = ["Amittai"]
__email__ = "Amittai.J.Wekesa.24@dartmouth.edu"
__github__ = "@siavava"

from CSP import CSP

from erratum import ( log_error, log_info, log_debug_info )
import heuristics

class CircuitComponent():
    def __init__(self, id, dx, dy):
        self.id = id
        self.dx = dx
        self.dy = dy
        
    def __eq__(self, other) -> bool:
        return self.id == other.id
                
    def __hash__(self):
        return hash(self.id)
    
    def __str__(self):
        return str(self.id)
                
    def get_cover(self, x, y, board_x, board_y):
        
        if x < 0 or y < 0:
            return None
        
        if (x + self.dx > board_x) or (y + self.dy > board_y):
            return None
            
        covered = set()
        
        for i in range(x, x + self.dx):
            for j in range(y, y + self.dy):
                covered.add((i, j))
        
        return covered
    
    def get_all_domains(self, board_x, board_y):
        all_domains = set()
        for i in range(board_x):
            for j in range(board_y):
                cover = self.get_cover(i, j, board_x, board_y)
                if cover: all_domains.add((i, j))
        return all_domains
    
    def does_not_overlap(self, other, assignments, board_x, board_y):
        pos_self = assignments.get(self, None)
        pos_other = assignments.get(other, None)
        
        if not pos_self or not pos_other:
            return True
        
        current_cover = self.get_cover(pos_self[0], pos_self[1], board_x, board_y)
        other_cover = other.get_cover(pos_other[0], pos_other[1], board_x, board_y)
        
        if not current_cover or not other_cover:
            return False
        
        intersection = current_cover & other_cover
        
        return len(intersection) == 0
        

class CircuitProblem(CSP):
    
    def __init__(self, x, y, variables=None, mrv=False, \
        degree_heuristic=False, lcv=False, inferences=False, debug=False):
        self.x = x
        self.y = y
        self.grid = ['.' * x] * y
        self.variables = set()
        self.needed_assignments = 0
        self.constraints = set()
        self.domains = {}
        
        for variable in variables:
            self.add_variable(variable)
            
            
        
        self.mrv = mrv
        self.degree_heuristic = degree_heuristic
        self.lcv = lcv
        self.inferences = inferences
        self.debug = debug
        
    def display(self, assignments: dict):
        
        if not assignments:
            return "\n".join(self.grid)
        
        string = ""
        
        log_debug_info(f"assignments: {assignments}")
        
        all_marked = {}
        for var in assignments.keys():
            char = var.id
            assignment = assignments[var]
            x, y = assignment[0], assignment[1]
            for ix in range(x, x+var.dx):
                for iy in range(y, y+var.dy):
                    all_marked[(ix, iy)] = char
                    log_debug_info(f"({ix}, {iy}): {char}")
        
        for iy in range(self.y):
            for ix in range(self.x):
                string += all_marked.get((ix, iy), ".")
            string += "\n"
        
        return string
    
    def __str__(self):
        return f"CSP: {self.variables}, {self.constraints}"
    
        
    def add_variable(self, var: tuple, domain=None):
        """
            Add a new variable into the CSP.
            variable is a tuple of the form `(id, dx, dy)`
        """
        
        _id = var[0]
        dx = var[1]
        dy = var[2]
        
        component = CircuitComponent(_id, dx, dy)
        self.variables.add(component)
        self.domains[component] = component.get_all_domains(self.x, self.y)
        for other_var in self.variables:
            if other_var != component:
                self.add_constraint(component, other_var)
        self.needed_assignments += 1
        
    def add_constraint(self, var1, var2):
        self.constraints.add((var1, var2))
        
    def get_domain(self, var: CircuitComponent) -> set:
        """Returns the domain for the given variable."""
        return self.domains[var]
    
    def satisfies_constraint(self, constraint: tuple, assignments: dict, variable: CircuitComponent, value):
        if len(constraint) != 2:
            if self.debug: log_error(f"Invalid constraint dimension: {constraint}")
            return False
        
        if variable not in constraint:
            return True
        
        other_variable: CircuitComponent = constraint[0] if constraint[0] != variable else constraint[1]
        
        if other_variable not in assignments:
            return True
        
        assignment: tuple = value
        other_assignment = assignments[other_variable]
        
        var_x, var_y = assignment[0], assignment[1]
        other_x, other_y = other_assignment[0], other_assignment[1]
        
        cover_a = variable.get_cover(var_x, var_y, self.x, self.y)
        cover_b = other_variable.get_cover(other_x, other_y, self.x, self.y)
        
        if not cover_a or not cover_b:
            return False
        
        intersection = cover_a & cover_b
        
        return len(intersection) == 0

    def is_consistent(self, assignments: dict, variable: CircuitComponent, value):
        
        log_info("consistency check")
        
        for constraint in self.constraints:
            if self.debug: log_error(f"Constraint: {constraint}")
            if variable not in constraint:
                continue
            elif not self.satisfies_constraint(constraint, assignments, variable, value):
                return False
        return True
    
    def order_values(self, var: CircuitComponent, assignment):
        if not self.lcv:
            return self.domains[var]
        
        unassigned_vars = [var for var in self.variables if var not in assignment]
        
        return heuristics.lcv_heuristic(self, var, unassigned_vars)
        
        
    def get_unassigned_variable(self, assignments):
        
        if not self.mrv:
            for var in self.variables:
                if var not in assignments:
                    return var
            return None
        
        else:
            unassigned = [var for var in self.variables if var not in assignments]
            return heuristics.mrv_heuristic(self, unassigned)
        
    def is_completed(self, assignments: dict):
        complete = len(assignments) == self.needed_assignments
        if complete:
            self.solution = assignments
            
        return complete

if __name__ == '__main__':
    cp = CircuitProblem(3, 3)
    cp.display()