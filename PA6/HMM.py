#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from Maze import Maze
from Matrix import Matrix

CORRECT_COLOR = .88                     # Robot reading accuracy probability = .88
WRONG_COLOR = 1 - CORRECT_COLOR         # Robot reading accuracy probability = .
MOVE_PROBABILITY = 1/4                  # 1/4 chance of moving in any direction

# I specified these in case a case might arise where
# a robot is more biased to move North than South, for instance.
# Then, I would just have to change the probabilities here.
NORTH_PROBABILITY = SOUTH_PROBABILITY = EAST_PROBABILITY = WEST_PROBABILITY = MOVE_PROBABILITY

class HMM:
    def __init__(self, filename):
        """
            Create a new HMM based on the given map file.
        """
        self.maze = Maze(filename)
        
        # initialize matrices for sensor probabilities of detecting each color.
        self.sensor_probabilities = dict()          # color -> probabilities of that color being read for each position in Maze
        for color in self.maze.colors:
            self.sensor_probabilities[color] = Matrix(self.maze.width, self.maze.height)
            
        self.transitions = None                                                     # transition probabilities between every possible position in Maze
        self.position_distribution = Matrix(self.maze.width, self.maze.height)      # probabilities of each position being the robot's starting position
        self.steps = []                                                             # list of matrices of probabilities for each step in the sequences
        self.initialize_probabilities() 
        
    def initialize_probabilities(self):
        """
        Initializes the probabilities dictionary.
        """
        possible_positions = self.maze.count_positions()
        
        if not possible_positions:
            raise ValueError('No possible positions in maze.')
                
        for x in range(self.maze.width):
            for y in range(self.maze.height):
                
                # save the sensor detection probabilities
                self.compute_sensor_values(x, y)
                        
                # Save the transition probabilities
                self.compute_transition_matrix(x, y)
                
                # Find the probability for robot's starting position being at current position
                self.compute_distribution(x, y, possible_positions)
                
    def compute_sensor_values(self, x, y):
        """
            Compute the transition matrix for the given x, y position.
        """
        # Save the state probabilities
        c = self.maze.get_char(x, y)
        if c and c != '#':
            for color in self.maze.colors:
                if color == c:
                    self.sensor_probabilities[color][x, y] = CORRECT_COLOR
                else:
                    self.sensor_probabilities[color][x, y] = WRONG_COLOR / (self.maze.color_count - 1)
   
    def compute_transition_matrix(self, x, y):
        """
            Return the transition matrix for the given x, y position.
        """
        
        current_index = self.maze.index(x, y)
        stay_put = 0
        matrix = Matrix(self.maze.count_positions(), self.maze.count_positions())
        
        north = self.maze.get_char(x, y - 1)
        north_index = self.maze.index(x, y - 1)
        
        south = self.maze.get_char(x, y + 1)
        south_index = self.maze.index(x, y + 1)
        
        east = self.maze.get_char(x + 1, y)
        east_index = self.maze.index(x + 1, y)
        
        west = self.maze.get_char(x - 1, y)
        west_index = self.maze.index(x - 1, y)
        
        if north and north != '#':
            matrix[north_index, current_index] = NORTH_PROBABILITY
        else:
            stay_put += NORTH_PROBABILITY
            
        if south and south != '#':
            matrix[south_index, current_index] = SOUTH_PROBABILITY
        else:
            stay_put += SOUTH_PROBABILITY
        if east and east != '#':
            matrix[east_index, current_index] = EAST_PROBABILITY
        else:
            stay_put += EAST_PROBABILITY
        if west and west != '#':
            matrix[west_index, current_index] = WEST_PROBABILITY
        else:
            stay_put += WEST_PROBABILITY
            
        matrix[current_index, current_index] = stay_put
        
        self.transitions = matrix
        
    def compute_distribution(self, x, y, total):
        """
            Compute the distribution for the given x, y position.
        """
        if self.maze.get_char(x, y) != '#':
            self.position_distribution[x, y] = 1 / total
            
    def forward(self, readings: list):
        
        for reading in readings:
            if reading not in self.maze.colors:
                raise ValueError(f"Invalid color: {reading} not in working set {self.maze.colors}")
            
        distribution = Matrix.copy(self.position_distribution)                  # probabilities of each position being the robot's starting position
        
        # reset sequences (might have been set on a previous run)
        if self.steps:
            self.steps = []
            
        # append starting position position to steps.
        self.steps.append(distribution)
        
        for step in range(len(readings)):
            
            # get current reading
            reading = readings[step]
            
            # update the distribution
            distribution = self.transitions * distribution
            
            distribution = self.sensor_probabilities[reading] * distribution
            
            self.sequences.append(distribution)
        
    
