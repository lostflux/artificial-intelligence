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
        """
            The CircuitComponent class representes a circuit component that can be placed on the board.
            :arg id: The circuit component ID -- must be a hashable type.
            :arg dx: The width of the circuit component.
            :arg dy: The height of the circuit component.
        """
        self.id = id
        self.dx = dx
        self.dy = dy
        
    def __eq__(self, other) -> bool:
        """
            Test for equality between two CircuitComponents.
        """
        return self.id == other.id
                
    def __hash__(self):
        """
            Get the hash value of the CircuitComponent.
            NOTE: Hashing is done based on the CircuitComponent ID.
        """
        return hash(self.id)
    
    def __str__(self):
        """
            Return a string representation of the CircuitComponent.
        """
        return str(self.id)
                
    def get_cover(self, x, y, board_x, board_y):
        """
            Get the set of all cells covered by the circuit component.
            :arg x: The x coordinate of the circuit component.
            :arg y: The y coordinate of the circuit component.
            :arg board_x: The width of the board.
            :arg board_y: The height of the board.
        """
        
        # if coordinates are negative, return None
        if x < 0 or y < 0:
            return None
        
        # if board placement at current position causes overflow,
        #   return None
        if (x + self.dx > board_x) or (y + self.dy > board_y):
            return None
            
        # loop over all covered positions and add them to a set of all covered positions
        covered = set()
        for i in range(x, x + self.dx):
            for j in range(y, y + self.dy):
                covered.add((i, j))
        
        # return computed set
        return covered
    
    def get_all_domains(self, board_x, board_y):
        """
            Given a circuit component, and board dimensions, 
            return a set of all valid placements for the component on the board.
            :arg board_x: The width of the board.
            :arg board_y: The height of the board.
        """
        
        # initialize set of all valid placements
        all_domains = set()
        
        # loop over all cells on the board, test placement.
        # If placement is valid, add it to the set of all valid placements.
        for i in range(board_x):
            for j in range(board_y):
                cover = self.get_cover(i, j, board_x, board_y)
                if cover: all_domains.add((i, j))
                
        # return set of all valid placements
        return all_domains
    
    def overlaps(self, self_pos, other, other_pos, board_x, board_y):
        """
            Given two circuit components, and their respective positions on the board,
            check whether the two components overlap.
            :arg self_pos: The position of the first circuit component.
            :arg other: The second circuit component.
            :arg other_pos: The position of the second circuit component.
            :arg board_x: The width of the board.
            :arg board_y: The height of the board.
        """
        
        # Get the cover for each component.
        current_cover = self.get_cover(self_pos[0], self_pos[1], board_x, board_y)
        other_cover = other.get_cover(other_pos[0], other_pos[1], board_x, board_y)
           
        # if any is empty, overlap impossible.
        if not current_cover or not other_cover:
            return False
        
        # Find the intersection of the two covers.
        intersection = current_cover & other_cover
        
        # if the intersection is empty, no overlap.
        return len(intersection) != 0
        

class CircuitProblem(CSP):
    
    def __init__(self, x, y, variables=None, mrv=False, \
        degree=False, lcv=False, inferences=False, debug=False):
        """
            Constructor for the Constrained Search Problem.
            :arg variables: A `set` of variables in the CSP.
            :arg domains: A `dictionary` of variables -> domains in the CSP.
            :arg constraints: A set of constraints in the CSP.
        """
        
        # initialize CSP
        self.x = x
        self.y = y
        self.grid = ['.' * x] * y
        self.variables = set()
        self.needed_assignments = 0
        self.solution = None
        
        # initialize attributes
        self.variable_mappings = dict()
        self.value_mappings = []
        self.variables = set()
        self.domains: list = []
        self.constraints = set()
        self.assignments = {}
        
        # initialize varibles
        for variable in variables:
            self.add_variable(variable)
        
        
        # enable or disable heuristics
        self.mrv = mrv
        self.degree = degree
        self.lcv = lcv
        
        # enable or disable debug mode
        self.debug = debug
        
    def initialize(self, variables, domains=None, constraints=None):
        """
            Sets up the variables in the CSP.
            : NOTE This is a CSP method retained for compatibility with the CSP interface,
            but the CircuitProblem class uses `add_variable` to set up variables.
        """
        pass
        
    def display(self, assignments=None):
        """
            Display the current state of the CSP.
            NOTE: This returns a string to the caller, akin to the str() function.
        """
        
        if assignments: self.assignments = assignments
        
        log_info(self)
    
    def __str__(self):
        
        string = "Circuit Board:\n\n"
        
        string += "\n".join(self.grid)
        
        string += "\n\nPlacements:\n\n"
        
        # if no assignments, return default board
        if not self.assignments:
            string += "\n".join(self.grid)
            return string
        
        # find all squares to be marked
        all_marked = {}
        for var in self.assignments.keys():
            char = self.variable_mappings[var].id
            assignment = self.value_mappings[self.assignments[var]]
            x, y = assignment[0], assignment[1]
            var = self.variable_mappings[var]
            for ix in range(x, x+var.dx):
                for iy in range(y, y+var.dy):
                    all_marked[(ix, iy)] = char
        
        # build board, marking components where squares are placed. 
        for iy in range(self.y):
            for ix in range(self.x):
                string += all_marked.get((ix, iy), ".")
            string += "\n"
            
        if self.debug:
            string += f"\n\n\tHeuristics enabled:\n"
            string += f"\t\tMRV: {self.mrv}\n"
            string += f"\t\tDegree: {self.degree}\n"
            string += f"\t\tLCV: {self.lcv}\n"
        
        # return string version of board.
        return string
    
        
    def add_variable(self, var: tuple, domain=None):
        """
            Add a new variable into the CSP.
            variable is a tuple of the form `(id, dx, dy)`
        """
        
        # Get the variable id, dx, and dy.
        _id = var[0]
        dx = var[1]
        dy = var[2]
        
        # create new component.
        component = CircuitComponent(_id, dx, dy)
        
        # add component info into CSP.
        index = len(self.variables)
        self.variable_mappings[index] = component
        self.variables.add(index)
        self.domains.append(set())
        all_values = component.get_all_domains(self.x, self.y)
        for value in all_values:
            if not value in self.value_mappings:
                self.value_mappings.append(value)
                
            val_index = self.value_mappings.index(value)
            self.domains[-1].add(val_index)
            
        
        # add constraint between component and all other components.
        for other_var_index in self.variables:
            if other_var_index != index:
                self.add_constraint(index, other_var_index)
                
        # increment needed assignments.
        self.needed_assignments += 1
        
    def add_constraint(self, var1, var2):
        """
            Add a new constraint between two variables.
        """
        self.constraints.add((var1, var2))
        
    def get_domain(self, var: CircuitComponent) -> set:
        """Returns the domain for the given variable."""
        return self.domains[var]
    
    def satisfies_constraint(self, constraint: tuple, assignments: dict, variable: int, value: int):
        """
            Check if a specific assignment to a variable satisfies the given constraint.
            :arg constraint: A tuple of the form `(var1, var2)`
            :arg assignments: A dictionary of assignments to variables.
            :arg variable: The variable to check.
            :arg value: The value to check.
        """
        
        # if variable is not in the constraint,
        # assignment is invariant to the constraint.
        # return true.
        if variable not in constraint:
            return True
        
        # get indices for other variable
        # Get corresponding components,
        # and check if the two components overlap.
        var_1_index = variable
        var_2_index = constraint[0] if constraint[0] != variable else constraint[1]
        
        # if other variable unassigned, we canot know of violations.
        # Return True.
        if not var_2_index in assignments: return True
        
        # Get positions.
        pos_1 = self.value_mappings[value]
        val_2 = value if var_2_index == variable else assignments[var_2_index]
        pos_2 = self.value_mappings[val_2]
        
        # Get circuit components.
        var_1: CircuitComponent = self.variable_mappings[var_1_index]
        var_2: CircuitComponent = self.variable_mappings[var_2_index]
        
        # return whether the two components overlap or not.
        return not var_1.overlaps(pos_1, var_2, pos_2, self.x, self.y)
        

    def is_consistent(self, assignments: dict, variable: int, value):
        """
            Check if a specific assignment to a variable is consistent with all constraints.
        """
        
        # for each constraint containing the variable, 
        # check if the assignment is consistent.
        for constraint in self.constraints:
            if variable not in constraint:
                continue
            elif not self.satisfies_constraint(constraint, assignments, variable, value):
                return False
        return True
    
    def order_values(self, var: CircuitComponent, assignment):
        """
            Order the values in the domain of the given variable based on the heuristic.
            :arg var: The variable to order.
        """
        
        # Return values for assignment to the current variable,
        # depending on whether LCV heuristic is enabled. 
        if not self.lcv:
            return self.domains[var]
        
        unassigned_vars = [var for var in self.variables if var not in assignment]
        
        return heuristics.lcv_heuristic(self, var, unassigned_vars)
        
        
    def get_unassigned_variable(self, assignments):
        """
            Get the next unassigned variable.
            :arg assignments: A dictionary of prior assignments to variables.
        """
        
        # select a next variable to assign, 
        # depending on whether MRV heuristic & Degree heuristic
        # are activated or not.
        if not self.mrv:
            for var in self.variables:
                if var not in assignments:
                    return var
            return None
        
        else:
            unassigned = [var for var in self.variables if var not in assignments]
            return heuristics.mrv_heuristic(self, unassigned, deg_heuristic=self.degree)
        
    def is_completed(self, assignments: dict):
        """
            Check if the CSP assignments are complete.
        """
        if len(assignments) == self.needed_assignments:
            self.solution = assignments
            return True
            
        return False
    
    def renders_unsolvable(self, var: int, value: int, other_var: int):
        """
            Given a pecific assignment, check if the CSP becomes unsolvable after the assignment.
        """
        
        # check every possible value for the adjacent variable. 
        # If none is compatible with teh current assignment, 
        # then the assignment will render the CSP unsolvable.
        
        component1: CircuitComponent = self.variable_mappings[var]
        
        position1 = self.value_mappings[value]
        component2 = self.variable_mappings[other_var]
        next_domain = self.domains[other_var]
        for other_value in next_domain:
            position2 = self.value_mappings[other_value]
            if not component1.overlaps(position1, component2, position2, self.x, self.y):
                return False
        
        return True

if __name__ == '__main__':
    cp = CircuitProblem(3, 3)
    cp.display()