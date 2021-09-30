#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""This module implements a Data Structure to store important information
    about a specific maze.
"""
__author__ = ["Amittai", "Alberto Quattrini Li"]
__copyright__ = "Copyright 2021"
__credits__ = ["Amittai", "Alberto Quattrini Li"]
__email__ = "Amittai.J.Wekesa.24@dartmouth.edu"
__github__ = "@siavava"

from time import sleep

# Maze.py
#  original version by db, Fall 2017
#  Feel free to modify as desired.

# Maze objects are for loading and displaying mazes, and doing collision checks.
#  They are not a good object to use to represent the state of a robot mazeworld search
#  problem, since the locations of the walls are fixed and not part of the state;
#  you should do something else to represent the state. However, each Mazeworldproblem
#  might make use of a (single) maze object, modifying it as needed
#  in the process of checking for legal moves.

# Test code at the bottom of this file shows how to load in and display
#  a few maze data files (e.g., "maze1.maz", which you should find in
#  this directory.)

#  the order in a tuple is (x, y) starting with zero at the bottom left

# Maze file format:
#    # is a wall
#    . is a floor
# the command \robot x y adds a robot at a location. The first robot added
# has index 0, and so forth.


class Maze:

    # internal structure:
    #   self.walls: set of tuples with wall locations
    #   self.width: number of columns
    #   self.rows

    def __init__(self, mazefilename):

        self.robotloc = []
        # read the maze file into a list of strings
        f = open(mazefilename)
        lines = []
        for line in f:
            line = line.strip()
            # ignore blank limes
            if len(line) != 0:
                if line[0] == "\\":
                    #print("command")
                    # there's only one command, \robot, so assume it is that
                    parms = line.split()
                    x = int(parms[1])
                    y = int(parms[2])
                    self.robotloc.append(x)
                    self.robotloc.append(y)
                    
                else:
                    lines.append(line)
                
        f.close()

        self.width = len(lines[0])
        self.height = len(lines)

        self.map = list("".join(lines))



    def index(self, x, y):
        return (self.height - y - 1) * self.width + x


    # returns True if the location is a floor
    def is_floor(self, x, y):
        if x < 0 or x >= self.width:
            return False
        if y < 0 or y >= self.height:
            return False

        return self.map[self.index(x, y)] == "."
    
    def can_move(self, x, y, current_state):
        """
            Check if a given point in the maze can be moved to.
            This method checks if the point is a valid room and doesn't have an occupant.
        """
        if self.is_floor(x, y):
            return not self.has_robot(x, y, state=current_state)
        
        return False


    def has_robot(self, x, y, state=None):
        if x < 0 or x >= self.width:
            return False
        if y < 0 or y >= self.height:
            return False
        
        # if unspecified state, use the stating locations for the robots.
        if state is None:
            state = self.robotloc

        # check to make sure the point has a robot.
        for i in range(0, len(state), 2):
            rx = state[i]
            ry = state[i + 1]
            if rx == x and ry == y:
                return True

        # if no match found, return False.
        return False


    # function called only by __str__ that takes the map and the
    #  robot state, and generates a list of characters in order
    #  that they will need to be printed out in.
    def create_render_list(self):
        renderlist = list(self.map)

        robot_number = 0
        for index in range(0, len(self.robotloc), 2):

            x = self.robotloc[index]
            y = self.robotloc[index + 1]

            renderlist[self.index(x, y)] = robotchar(robot_number)
            robot_number += 1

        return renderlist



    def __str__(self):

        # render robot locations into the map
        renderlist = self.create_render_list()

        # use the renderlist to construct a string, by
        #  adding newlines appropriately

        s = ""
        for y in range(self.height - 1, -1, -1):
            for x in range(self.width):
                s+= renderlist[self.index(x, y)]

            s += "\n"

        return s


def robotchar(robot_number):
    return chr(ord("A") + robot_number)


# A unit test for the Maze class.
def unit_test():
    test_maze1 = Maze("maze1.maz")
    print(test_maze1)

    test_maze2 = Maze("maze2.maz")
    print(test_maze2)

    test_maze3 = Maze("maze3.maz")
    print(test_maze3)

    print(test_maze3)
    print(test_maze3.robotloc)

    print(test_maze3.is_floor(2, 3))
    print(test_maze3.is_floor(-1, 3))
    print(test_maze3.is_floor(1, 0))

    print(test_maze3.has_robot(1, 0))

if __name__ == "__main__":
    unit_test()
