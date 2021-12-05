#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    This file implements basic unit tests for the integration 
    between the SensorlessProblem module, the Maze module, and the A* algorithm.
"""
__author__ = "Amittai"
__copyright__ = "Copyright 2021"
__credits__ = ["Amittai", "Alberto Quattrini Li"]
__email__ = "Amittai.J.Wekesa.24@dartmouth.edu"
__github__ = "@siavava"


from SensorlessProblem import SensorlessProblem
from Maze import Maze

# null heuristic, useful for testing astar search without heuristic (uniform cost search).
def null_heuristic(state):
    return 0

def test(map_file, animate=True):
    test_maze = Maze(map_file)
    test_prob = SensorlessProblem(test_maze)
    solution = test_prob.locate()
    if solution.path and animate:
        test_prob.animate_path(solution.path)
        
    print(solution)
    if solution.path:
        print(f"Directions to take:\n{test_prob.get_directions(solution.path)}")
        print(f"Final position = {test_prob.get_final_position(solution.path)}")
        

def main():
    """
        This method is triggered to run when one runs the file.
    """
    # Test problems
    
    m3 = "mazes/maze3.maz"
    m4 = "mazes/maze4.maz"
    
    # Note: maze 5 to 9 are variations of the same mazee with increasing complexity.
    m5 = "mazes/maze5.maz"
    m6 = "mazes/maze6.maz"
    m7 = "mazes/maze7.maz"
    m8 = "mazes/maze8.maz"
    m9 = "mazes/maze9.maz"
    
    
    ####################################################
    ### un-mute one of these tests to run it.        ###
    ### NOTE: running all at a go will take a while. ###
    ### You may wish to simplify the goal,           ###
    ### especially on the more advanced mazes.       ###
    ### NOTE: Turning off the `animate` flag         ###
    ### will turn off playing path animations.       ###
    ####################################################
    
    # Test on Maze 3
    # test(m3, animate=True)
    
    # # Test on Maze 4
    # test(m4, animate=True)
    
    # # Test on Maze 5
    test(m5, animate=True)
    
    # # Test on Maze 6
    # test(m6, animate=False)
    
    # # Test on Maze 7
    # test(m7, animate=False)
    
    # # Test on Maze8
    # test(m8, animate=False)
    
    # # Test on Maze9
    # test(m9, animate=False)
    
    #######################################################
    ### These additional tests are on Maps we developed ###
    ### in my Spring CS50 class. ##########################
    ### They are more complicated. ########################
    ### Correct behavior is not assured. ##################
    #######################################################

if __name__ == "__main__":
    main()