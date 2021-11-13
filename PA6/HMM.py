#!/usr/bin/env python3

from Maze import Maze
from Matrix import Matrix

CORRECT_COLOR = .88                     # Robot reading accuracy probability = .88
WRONG_COLOR = 1 - CORRECT_COLOR         # Robot reading accuracy probability = .
MOVE_PROBABILITY = 1/4                  # 1/4 chance of moving in any direction

class HMM:
    def __init__(self, mazefilename):
        
        self.maze = Maze(mazefilename)
        
        self.sensor_probabilities = dict()
        self.initialize_probabilities()
        
    def initialize_probabilities(self):
        """
        Initializes the probabilities dictionary.
        """
        
        # Initialize the probabilities dictionary.
        # The keys are colors in the Maze
        # The values Matrices representing probabilities.
        
        all_colors = self.maze.colors
        self.COLOR_COUNT = len(all_colors)
        for color in all_colors.maze.colors:
            self.sensor_probabilities[color] = Matrix(self.maze.width, self.maze.height)
            
        self.transitions = [Matrix(self.maze.possible_states()) for i in ]
        
                
        for x in range(self.maze.width):
            for y in range(self.maze.height):
                
                # Save the state probabilities
                c = self.maze.get(x, y)
                if c != '#':
                    for color in all_colors:
                        if color == c:
                            self.sensor_probabilities[color][x, y] = CORRECT_COLOR
                        else:
                            self.sensor_probabilities[color][x, y] = WRONG_COLOR / (self.COLOR_COUNT - 1)
                        
                # Save the transition probabilities
                pos_moves = self.maze.check_neighbors(x, y)
                for direction in range(len(pos_moves)):
                    possible = pos_moves[direction]
                    
                    if direction == 0: 
                
                        
        
                
        
        
                        
            
                
    
    

    def train(self, observations, states):
        """
        Train the HMM with the given observations and states.
        :param observations: A list of observations.
        :param states: A list of states.