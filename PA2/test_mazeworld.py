#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    This file implements basic unit tests for the integration 
    between the MazeworldProblem module, the Maze module, and the A* algorithm.
"""
__author__ = "Amittai"
__copyright__ = "Copyright 2021"
__credits__ = ["Amittai", "Alberto Quattrini Li"]
__email__ = "Amittai.J.Wekesa.24@dartmouth.edu"
__github__ = "@siavava"


from MazeworldProblem import MazeworldProblem
from Maze import Maze
from astar_search import astar_search

# null heuristic, useful for testing astar search without heuristic (uniform cost search).
def null_heuristic(state):
    return 0

def test(map_file, final_state, animate=True):
    test_maze = Maze(map_file)
    test_mp = MazeworldProblem(test_maze, final_state)
    solution = astar_search(test_mp, test_mp.manhattan_heuristic)
    if solution.path:
        test_mp.animate_path(solution.path)
    print(solution)

def main():
    """
        This method is triggered to run when one runs the file.
    """
    # Test problems
    
    m3, final3 = "mazes/maze3.maz", (1, 4, 1, 3, 1, 2)
    m4, final4 = "mazes/maze4.maz", (22, 1, 17, 2)
    
    # Note: maze 5 to 9 are variations of the same mazee with increasing complexity.
    m5, final5 = "mazes/maze5.maz", (13, 13, 1, 13, 13, 1, 1, 1)
    m6, final6 = "mazes/maze6.maz", (13, 13, 1, 13, 13, 1, 1, 1)
    m7, final7 = "mazes/maze7.maz", (13, 13, 1, 13, 13, 1, 1, 1)
    m8, final8 = "mazes/maze8.maz", (13, 13, 1, 13, 13, 1, 1, 1)
    m9, final9 = "mazes/maze9.maz", (13, 13, 1, 13, 13, 1, 1, 1)
    m10, final10 = "mazes/maze10.maz", (2, 1, 3, 1, 1, 2, 2, 2, 3, 2, 1, 3, 2, 3, 3, 3)
    m11, final11 = "mazes/hole.maz", (16, 3, 5, 5)
    
    
    ####################################################
    ### un-mute one of these tests to run it.        ###
    ### NOTE: running all at a go will take a while. ###
    ### You may wish to simplify the goal,           ###
    ### especially on the more advanced mazes.       ###
    ### NOTE: Turning off the `animate` flag         ###
    ### will turn off playing path animations.       ###
    ####################################################
    
    # Test on Maze 3
    # test(m3, final3)
    
    # # Test on Maze 4
    # test(m4, final4)
    
    # # Test on Maze 5
    test(m5, final5)
    
    # # Test on Maze 6
    # test(m6, final6)
    
    # # Test on Maze 7
    # test(m7, final7)
    
    # # Test on Maze8
    # test(m8, final8)
    
    # Test on Maze9
    # test(m9, final9)
    
    #######################################################
    ### These additional tests are on Maps we developed ###
    ### in my Spring CS50 class. ##########################
    ### They are more complicated. ########################
    ### Correct behavior is not assured. ##################
    #######################################################
    
    # test 8-puzzle version.
    # NOTE: The final position of the puzzle is inverted due to the coordinate system used by the game.
    # test(m10, final10)
    
    # test maze with bridges and holes
    # NOTE: Couldn't get this to work probably because of how the map is :(
    # test(m11, final11)
    

if __name__ == "__main__":
    main()