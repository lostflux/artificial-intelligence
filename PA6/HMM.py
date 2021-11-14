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
        self.sensor_probabilities = dict()
        for color in self.maze.colors:
            self.sensor_probabilities[color] = Matrix(self.maze.width, self.maze.height)
            
        self.transitions = dict()
        self.position_distribution = Matrix(self.maze.width, self.maze.height)
        self.color_count
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
        
        stay_put = 0
        matrix = Matrix(x, y)
        north = self.maze.get_char(x, y - 1)
        south = self.maze.get_char(x, y + 1)
        east = self.maze.get_char(x + 1, y)
        west = self.maze.get_char(x - 1, y)
        
        if north and north != '#':
            matrix[x, y - 1] = NORTH_PROBABILITY
        else:
            stay_put += NORTH_PROBABILITY
            
        if south and south != '#':
            matrix[x, y + 1] = SOUTH_PROBABILITY
        else:
            stay_put += SOUTH_PROBABILITY
        if east and east != '#':
            matrix[x + 1, y]= EAST_PROBABILITY
        else:
            stay_put += EAST_PROBABILITY
        if west and west != '#':
            matrix[x - 1, y]= WEST_PROBABILITY
        else:
            stay_put += WEST_PROBABILITY
            
        matrix[x, y] = stay_put
        
        self.transitions[(x, y)] = matrix
        
    def compute_distribution(self, x, y, total):
        """
            Compute the distribution for the given x, y position.
        """
        if self.maze.get_char(x, y) != '#':
            self.position_distribution[x, y] = 1 / total
    
