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

class SensorlessProblem(MazeworldProblem):

    ## You write the good stuff here:
    
    def __init__(self, maze, start_state=(0, 0, 1, 1, 2, 2, 3, 3)):
        self.maze = maze
        self.start_state = tuple(maze.robotloc)
        self.visited_states = 0

    def __str__(self):
        string =  "Blind robot problem: "
        string += "Possible start locations: " + str(self.start_state) + "\n"
        string += "Goal state:" + str(self.goal_locations) + "\n"
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
            
    def is_solved(self, state):
        return len(state) == 1
    
    def random_point(self):
        
        x, y = -1, -1
        
        while not self.maze.can_move((x, y)):
            x = randint(0, self.map.width - 1)
            y = randint(0, self.map.height - 1)
        
        return (x, y)
    
    def hunt(self, start_state=None, end=None):
        
        if not start_state:
            start_state = self.start_state
        if not end:
            end = [1, 1]
            
        results = []
        
        for state in start_state:
            if state == end:
                results.append(state)
            else:
                solution = astar_search(self.map, self.manhattan_heuristic)
                if solution.path:
                    results.append(end)
                else:
                    results.append(start_state)
                
        return tuple( set(results) )


    def locate(self, state=None):
        if state is None:
            state = self.start_state
            
        while not self.is_solved(state):
            goal_location = self.random_point()
            state = self.hunt(start_state=state, end=goal_location)
            
        return state
            
            
            


## A bit of test code

if __name__ == "__main__":
    test_maze3 = Maze("maze3.maz")
    test_problem3 = SensorlessProblem(test_maze3)
    
    final_state = test_problem3.locate()
    
    print(f"Final state = {final_state}")
    
