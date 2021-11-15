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


class Maze:
    """
        This class is used to represent the maze in a more readable way.\n
        NOTE: My y coordinates increase downward (it was just easier to use it this way),\n
        So while checking positions in a maze, make sure you are checking y the correct way.\n
        NOTE: Indices are 0-indexed.
    """

    def __init__(self, mazefilename):
        """
            Initializes a maze from a file.
        """
        # initialize array of map values.
        self.map = []
        self.colors = set()
        self.color_count = 0
        
        # open maze file. exits if failed.
        with open(mazefilename) as f:
            
            # for each line in the file,
            for line in f:
                
                # remove trailing / beginning spaces
                line = line.strip().lower()
                
                # if blank, skip
                # otherwise, save the line
                # and index unique colors in the line.
                if len(line) != 0:
                    self.map.append(line)
                    self.colors |= set(line)
                    
            self.colors.discard("#")
            self.color_count = len(self.colors) 
            f.close()

        # get the width and height of the maze
        self.width = len(self.map[0])
        self.height = len(self.map)

    def index(self, x, y):
        """
            Get the referential index corresponding to a given point on the map.\n
        """
        if 0 <= x < self.width and 0 <= y < self.height:
            return y * self.width + x
        return None
    
    def de_index(self, index):
        """
            Given a referential index into the Maze,\n
            returns the corresponding x and y coordinates.\n
        """
        return (int(index % self.width), int(index // self.width))


    def get_char(self, x, y):
        """
            Get the character at given position in the Maze.
        """
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.map[y][x]
        
        return None
    
    def count_positions(self):
        """
            Get the total number of positions in the Maze.\n
            This is just a convenience function,\n
            and does not actually check whether a position can be occupied.\n
            For that, use `valid_positions()`.
        """
        return self.width * self.height
    
    def valid_positions(self):
        """
            Get the list of valid positions in the Maze.\n
            This function does not count positions that cannot be occupied.\n
            To get a count of all positions without regard to occupiability,\n
            use `count_positions()`.
        """
        count = 0
        for x in range(self.width):
            for y in range(self.height):
                if self.get_char(x, y) != "#":
                    count += 1
                    
        return count
        
    def __str__(self):
        """
            Return a string representation of the Maze.\n
        """        
        s = ""
        for line in self.map:
            s += line + "\n"
        return s


# A unit test for the Maze class.
def unit_test():
    test_maze1 = Maze("mazes/maze1.maz")
    print(test_maze1)

    test_maze2 = Maze("mazes/maze2.maz")
    print(test_maze2)

    test_maze3 = Maze("mazes/maze3.maz")
    print(test_maze3)

    print(test_maze3)

if __name__ == "__main__":
    unit_test()
