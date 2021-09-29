#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""This module implements a MazeworldProblem data structure 
    to represent a maze world state.
"""
__author__ = "Amittai"
__copyright__ = "Copyright 2021"
__credits__ = ["Amittai", "Alberto Quattrini Li"]
__email__ = "Amittai.J.Wekesa.24@dartmouth.edu"
__github__ = "@siavava"

from Maze import Maze
from time import sleep

class MazeworldProblem:

    ## you write the constructor, and whatever methods your astar function needs

    def __init__(self, maze, goal_locations):
        self.maze = maze
        self.goal_locations = goal_locations
        self.start_state = tuple(maze.robotloc)
        self.visited_states = 0


    def __str__(self):
        string = "Mazeworld problem:\n"
        string += "Goal state:" + str(self.goal_locations) + "\n"
        string += "Maze:\n" + str(self.maze) + "\n"
        return string

    def get_successors(self, state):
        """
        Returns a list of (action, state, cost) tuples corresponding to edges in the graph.
        """
        successors = []
        
        num_bots = len(state) // 2
            
        pos_steps = [-1, 1]
        for bot in range(num_bots):
            x = state[2*bot]
            y = state[2*bot + 1]
            for dx in pos_steps:
                
                if self.maze.can_move(x+dx, y):
                    index = 2*bot
                    new_state = self.move(state, index=index, new_val=x+dx)
                    if new_state:
                        successors.append(new_state)
                    
            for dy in pos_steps:
                
                if self.maze.can_move(x, y+dy):
                    index = 2*bot + 1
                    new_state = self.move(state, index=index, new_val=y+dy)
                    if new_state:
                        successors.append(new_state)
        
        print(f"Successors: {successors}")
        return successors
    
    # @staticmethod
    def move(self, state, index=None, new_val=None):
        """
        Given a state and an action, returns the new state.
        """
        if not index or not new_val:
            return None
        
        next_state = []
        for i in range(len(state)):
            if i == index:
                next_state.append(new_val)
            else:
                next_state.append(state[i])
                
        return tuple(next_state)
                
    def is_goal(self, state):
        return state in self.goal_locations

    # given a sequence of states (including robot turn), modify the maze and print it out.
    #  (Be careful, this does modify the maze!)
    def animate_path(self, path):
        # reset the robot locations in the maze
        self.maze.robotloc = tuple(self.start_state[1:])

        for state in path:
            print(str(self))
            self.maze.robotloc = tuple(state[1:])
            sleep(1)

            print(str(self.maze))
            
    def manhattan_heuristic(self, state):
        
        if not state:
            return 0
        
        acc = 0
        for i in range(0, len(state), 2):
            x, goal_x = state[i], self.goal_locations[i]
            y, goal_y = state[i + 1], self.goal_locations[i + 1]
            acc = acc +  abs(goal_x - x) + abs(goal_y - y)
            
        return acc


## A bit of test code. You might want to add to it to verify that things
#  work as expected.

if __name__ == "__main__":
    test_maze3 = Maze("maze3.maz")
    test_mp = MazeworldProblem(test_maze3, (1, 4, 1, 3, 1, 2))

    print(test_mp.get_successors((0, 1, 0, 1, 2, 2, 1)))
