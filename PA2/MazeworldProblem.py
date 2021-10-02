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
        
        # Initialzie successors, 
        # loop over all bots and find their possible next movements,
        # and add them to the array of possible next states.
        
        successors = []
        num_bots = len(state) // 2
        
        for bot in range(num_bots):
            ix = 2 * bot
            iy = ix + 1
            x, y = state[ix], state[iy]
            
            for step in [-1, 1]:
                # if bot can move in x direction, add to successors.
                if self.maze.can_move(x+step, y, state):
                    
                    new_state = self.move(state, index=ix, new_val=x+step)
                    successors.append(new_state)
                    
                # if bot can move in y direction, add to successors.
                if self.maze.can_move(x, y+step, state):
                    
                    new_state = self.move(state, index=iy, new_val=y+step)
                    successors.append(new_state)

        # return compiled array of successors
        return successors
    
    def move(self, state, index=None, new_val=None):
        """
            Given a state and an action, returns the new state.
        """
        
        # initialize next state 
        next_state = []
        
        # copy values from original state, swapping out the value at index with new_val
        for i in range(len(state)):
            if i == index:
                next_state.append(new_val)
            else:
                next_state.append(state[i])
                
        # return an immutable tuple of the new state.
        return tuple(next_state)
                
    def is_goal(self, state):
        """
            Check if a given state is the goal state for a game instance.
        """
        
        # loop over the state, checking if all positions match the goal state.
        for i in range(len(state)):
            if state[i] != self.goal_locations[i]:
                return False
        return True


    def animate_path(self, path):
        """
            Given a sequence of states (including robot turn), modify the maze and print it out.
            (Be careful, this does modify the maze!)
        """
        
        # reset the robot locations in the maze
        self.maze.robotloc = tuple(self.start_state)

        for state in path:
            print(str(self))
            self.maze.robotloc = tuple(state)
            sleep(1)

            print(str(self.maze))
            
    def manhattan_heuristic(self, state):
        """
            Calculate the manhattan distance between the current state and the goal state.
        """
        
        if not state:
            return 0
        
        # accumulate the sum of the distances between the robot 
        # and its corresponding goal locaiton.
        acc = 0
        for i in range(0, len(state), 2):
            x, goal_x = state[i], self.goal_locations[i]
            y, goal_y = state[i + 1], self.goal_locations[i + 1]
            acc = acc + abs(goal_x - x) + abs(goal_y - y)
            
        # return the accumulated sum.
        return acc


# A unit test for the MazeworldProblem class.
def unit_test():
    test_maze3 = Maze("maze5.maz")
    test_mp = MazeworldProblem(test_maze3, (13, 13, 1, 13, 13, 1, 1, 1))

    print(test_mp.get_successors((0, 1, 0, 1, 2, 2, 1)))
    
    # test_maze4 = Maze("maze4.maz")
    # test_mp4 = MazeworldProblem(test_maze4, (20, 1))
    # print(test_mp4.get_successors((5, 1)))


if __name__ == "__main__":
   unit_test()
