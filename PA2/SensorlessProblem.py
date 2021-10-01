#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""This module implements a SensorlessProblem data structure 
    to represent help a robot pin down its location in a maze.
"""
__author__ = "Amittai"
__copyright__ = "Copyright 2021"
__credits__ = ["Amittai", "Alberto Quattrini Li"]
__email__ = "Amittai.J.Wekesa.24@dartmouth.edu"
__github__ = "@siavava"

from Maze import Maze
from time import sleep
from MazeworldProblem import MazeworldProblem
from astar_search import astar_search
from random import randint

class SensorlessProblem():

    ## You write the good stuff here:
    
    def __init__(self, maze, start_state=(0, 0, 1, 1, 2, 2, 3, 3)):
        self.maze = maze
        self.start_state = tuple(maze.robotloc)
        self.visited_states = 0
        self.actions = []

    def __str__(self):
        string =  "Blind robot problem: "
        string += "Possible start locations: " + str(self.start_state) + "\n"
        # string += "Goal state:" + str(self.goal_locations) + "\n"
        string += "Maze:\n" + str(self.maze) + "\n"
        return string


        # given a sequence of states (including robot turn), modify the maze and print it out.
        #  (Be careful, this does modify the maze!)

    def animate_path(self, path):
        # reset the robot locations in the maze
        self.maze.robotloc = tuple(self.start_state)

        for state in path:
            print(str(self))
            self.maze.robotloc = tuple(state)
            sleep(1)

            print(str(self.maze))
            
    def is_goal(self, state):
        
        _state = self._state(state)
        
        return len(_state) == 1
    
    def _state(self, state):
        _state = set()
        for i in range(0, len(state), 2):
            _state.add( (state[i], state[i+1]) )
            
        return _state
    
    
    def locate(self):
            
        solution = astar_search(self, self.manhattan_heuristic)
        
        print(f"Final *sure* position: {solution.path[-1]}")
        
        print(solution)
        
        final_state = self._state(solution.path[-1])
        
        (pos,) = final_state
        return pos
            
            
    def get_successors(self, state):
        """
        Returns a list of (action, state, cost) tuples corresponding to edges in the graph.
        """
        
        # Initialzie successors, 
        # for each possible robot location, attempt to move it
        # in the appropriate direction.
        successors = []
        
        for step in [-1, 1]:
            
            next_state_x = self.move(state, step, dir_x=True)
            next_state_y = self.move(state, step, dir_y=True)
            if next_state_x:
                successors.append(next_state_x)
                
            if next_state_y:
                successors.append(next_state_y)


        # return compiled array of successors
        return successors

    
    def move(self, state, step, dir_x=False, dir_y=False):
        """
            Given a state and an action, returns the new state.
        """
        
        # initialize next state 
        next_state = []
        
        # copy values from original state, swapping out the value at index with new_val
        for i in range(0, len(state), 2):
            
            ix, iy = i, i+1
            if dir_x and self.maze.is_floor(state[ix]+step, state[iy]):
                next_state.append(state[ix]+step)
                next_state.append(state[iy])
                continue
                
            elif dir_y and self.maze.is_floor(state[ix], state[iy]+step):
                next_state.append(state[ix])
                next_state.append(state[iy]+step)
                continue
            
            next_state.append(state[ix])
            next_state.append(state[iy])


        # return an immutable tuple of the new state.
        if state == next_state:
            return None
            
        return tuple(next_state)
      
    def manhattan_heuristic(self, state):
        """
            Calculate the manhattan distance for the set of bots using the max and min x and y coordinates.
        """
        max_x, max_y = 0, 0
        min_x, min_y = 0, 0
        
        for i in range(0, len(state), 2):
            ix, iy = i, i+1
            max_x = max(max_x, state[ix])
            min_x = min(min_x, state[ix])
            
            max_y = max(max_y, state[iy])
            min_y = min(min_y, state[iy])
                
        return abs(max_x - min_x) + abs(max_y - min_y)
                  


## A bit of test code

if __name__ == "__main__":
    test_maze3 = Maze("maze3.maz")
    test_problem3 = SensorlessProblem(test_maze3)
    
    final_state = test_problem3.locate()
    
    print(f"Final state = {final_state}")
    
