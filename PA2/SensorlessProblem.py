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
from astar_search import astar_search

class SensorlessProblem():

    ## You write the good stuff here:
    
    def __init__(self, maze):
        self.maze = maze
        self.start_state = tuple(maze.robotloc)
        self.visited_states = 0
        self.actions = []

    def __str__(self):
        string =  "Blind robot problem: "
        string += "Possible start locations: " + str(self.start_state) + "\n"
        string += "Maze:\n" + str(self.maze) + "\n"
        return string


    def animate_path(self, path):
        """
            Given a path, animate the robot following it.
        """
        self.maze.robotloc = tuple(self.start_state)

        for state in path:
            print(str(self))
            self.maze.robotloc = tuple(state)
            sleep(1)

            print(str(self.maze))
           
    def is_goal(self, state):
        """
            Given a state, returns True if it is a goal state,
            i.e. all the robot start locations have converged.
        """
        _state = self._state(state)
        return len(_state) == 1
    
    def _state(self, state):
        """
            This method, given a final state, collapses the locations into a tuple of unique items.
            This method is used internally and should not be used from outside the module.
            :arg state: The state to be converged.
        """
        
        _state = set()
        for i in range(0, len(state), 2):
            _state.add( (state[i], state[i+1]) )
            
        return tuple(_state)    
    
    def locate(self):
        """
            This method runs A* search on the current problem and returns the solution.
            I found it easier than having to call A* each time.
        """
        solution = astar_search(self, self.manhattan_heuristic)
        return solution
    
    def get_final_position(self, path):
        """
            Given a path, return the final position.
            :arg path: Path to follow.
        """
        final_state = self._state(path[-1])
        (pos,) = final_state
        return pos
    
    def get_directions(self, path) -> list:
        """
            Given a path, return a list of directions.
            :arg path: Path to follow.
        """
        
        # Initialzie directions array,
        # Step through the path, determine which direction 
        # was taken at each successive step and append it to the array.
        directions = []
        
        for i in range(len(path)-1):
            state = path[i]
            next_state = path[i+1]
            
            for ix in range(0, len(state), 2):
                
                if next_state[ix] > state[ix]:
                    directions.append("E")
                    break
                    
                elif next_state[ix] < state[ix]:
                    directions.append("W")
                    break
                
                elif next_state[ix+1] > state[ix+1]:
                    directions.append("N")
                    break
                
                elif next_state[ix+1] < state[ix+1]:
                    directions.append("S")
                    break

        return directions
            
            
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
        # For each possible direction of movement,
        # attempt to move every robot in that direction.
        # If resulting state is distinct from the current state (i.e. someone moved),
        # return it as a valid state.
        # NOTE: collisions are allowed -- 
        # since the ultimate goal is to converge all the robots into a single point, anyway.
        
        next_state = []
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


        # if no one moved, discard the state.
        if state == next_state:
            return None
            
        #return immutable copy of the state.
        return tuple(next_state)
      
    def manhattan_heuristic(self, state):
        """
            Calculate the manhattan distance for the set of bots using the max and min x and y coordinates.
        """
        
        # rather than using the normal Manhattan distance, we seek to box in all the robots
        # by finding the max and min coordinates in either both directions 
        # then using those to calculate the heuristic.
        
        
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
    import sys

    print("Run 'test_sensorless.py' to test the SensorlessProblem module.", file=sys.stderr)

