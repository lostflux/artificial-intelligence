#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    This module contains an HMM class for robot location.\n
"""

__author__ = ["Amittai"]
__copyright__ = "Copyright 2021"
__credits__ = ["Amittai"]
__email__ = "Amittai.J.Wekesa.24@dartmouth.edu"
__github__ = "@siavava"

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
        self.total_positions = self.maze.count_positions()
        if not self.total_positions:
            raise ValueError('No possible positions in maze.')
        
        # initialize matrices for sensor probabilities of detecting each color.
        self.sensor_probabilities = dict()          # color -> probabilities of that color being read for each position in Maze
        for color in self.maze.colors:
            self.sensor_probabilities[color] = Matrix(self.total_positions, self.total_positions)
            
        self.transitions = Matrix(self.maze.count_positions(), self.maze.count_positions())                                                   # transition probabilities between every possible position in Maze
        self.position_distribution = Matrix(self.maze.width, self.maze.height)      # probabilities of each position being the robot's starting position
        self.steps = []                                                             # list of matrices of probabilities for each step in the sequences
        self.initialize_probabilities() 
        
    def initialize_probabilities(self):
        """
        Initializes the probabilities dictionary.
        """
        self.position_distribution = Matrix(self.total_positions, 1)
        

                
        for x in range(self.maze.width):
            for y in range(self.maze.height):
                
                curr_char = self.maze.get_char(x, y)
                
                if curr_char is not None and curr_char != '#':
                
                    # save the sensor detection probabilities
                    self.compute_sensor_values(x, y)
                            
                    # Save the transition probabilities
                    self.compute_transition_matrix(x, y)
                    
                    # Find the probability for robot's starting position being at current position
                    index = self.maze.index(x, y)
                    self.position_distribution[index, 0] = 1 / self.total_positions
                
    def compute_sensor_values(self, x, y):
        """
            Compute the transition matrix for the given x, y position.
        """
        
        pos = self.maze.index(x, y)
        # Save the state probabilities
        c = self.maze.get_char(x, y)
        if c and c != '#':
            for color in self.maze.colors:
                if color == c:
                    self.sensor_probabilities[color][pos, pos] = CORRECT_COLOR
                else:
                    self.sensor_probabilities[color][pos, pos] = WRONG_COLOR / (self.maze.color_count - 1)
   
    def compute_transition_matrix(self, x, y):
        """
            Return the transition matrix for the given x, y position.
        """
        
        curr = self.maze.get_char(x, y)
        current_index = self.maze.index(x, y)
        
        if curr is not None and curr != '#':
            print("curr = %s" % curr)
            stay_put = 0
            
            north = self.maze.get_char(x, y - 1)
            north_index = self.maze.index(x, y - 1)
            
            south = self.maze.get_char(x, y + 1)
            south_index = self.maze.index(x, y + 1)
            
            east = self.maze.get_char(x + 1, y)
            east_index = self.maze.index(x + 1, y)
            
            west = self.maze.get_char(x - 1, y)
            west_index = self.maze.index(x - 1, y)
            
            if north is not None and north != '#':
                print(f"North char = {north}")
                self.transitions[north_index, current_index] = NORTH_PROBABILITY
            else:
                stay_put += NORTH_PROBABILITY
                
            if south is not None and south != '#':
                self.transitions[south_index, current_index] = SOUTH_PROBABILITY
            else:
                stay_put += SOUTH_PROBABILITY
            if east is not None and east != '#':
                self.transitions[east_index, current_index] = EAST_PROBABILITY
            else:
                stay_put += EAST_PROBABILITY
            if west is not None and west != '#':
                self.transitions[west_index, current_index] = WEST_PROBABILITY
            else:
                stay_put += WEST_PROBABILITY
                
            self.transitions[current_index, current_index] = stay_put
        
    def compute_distribution(self, x, y, total):
        """
            Compute the distribution for the given x, y position.
        """
        if self.maze.get_char(x, y) != '#':
            self.position_distribution[x, y] = 1 / total
            
    def forward(self, readings: str):
        
        readings = readings.lower()
        
        for reading in readings:
            if reading not in self.maze.colors:
                raise ValueError(f"Invalid color: {reading} not in working set {self.maze.colors}")
            
        distribution = Matrix.copy(self.position_distribution)                  # probabilities of each position being the robot's starting position
        
        # print(f"Initial = {distribution}")
        # reset sequences (might have been set on a previous run)
        if self.steps:
            self.steps = []
            
        # append starting position position to steps.
        self.steps.append(distribution)
        
        for step in range(len(readings)):
            
            # get current reading
            reading = readings[step]
            
            # update the distribution  
            distribution = self.sensor_probabilities[reading] * (self.transitions.transpose() * distribution)
            
            Matrix.normalize(distribution)
            
            self.steps.append(distribution)
            
            
            
    def backward(self, readings: str):
        """
            Compute the probability of the robot ending up in each position
            after the given readings.
        """
        readings = readings.lower()
        
        vector = Matrix.ones(self.maze.count_positions(), 1)
        if not self.steps:
            self.forward(readings)
            
        for step in range(len(self.steps) - 1, 0, -1):
            self.steps[step] = Matrix.multiply(self.steps[step], vector)
            Matrix.normalize(self.steps[step])
            
            vector = self.transitions * (self.sensor_probabilities[readings[step - 1]] * vector)
            
    def viterbi(self, readings: str):
        """
            Compute the most likely sequence of states for the given readings.
        """
        
        # normalize readings
        readings = readings.lower()                         # y
        
        # get transition matrix
        transitions = self.transitions                      # A
        
        # get emission matrices
        emissions = self.sensor_probabilities               # B
        
        # get initial distribution
        initial_probabilities = self.position_distribution  # pi
        
        delta = Matrix.zeros(len(readings), self.total_positions)
        predecessors = Matrix.copy(delta)
        
        for pos in range(self.total_positions):
            delta[0, pos] = initial_probabilities[pos, 0] * transitions[pos, pos]
            
            
        for t in range(1, len(readings)):
            for curr in range(self.total_positions):
                for prev in range(self.total_positions):
                    if delta[t, curr] < delta[t-1, prev] * transitions[prev, curr]:
                        delta[t, curr] = delta[t-1, prev] * transitions[prev, curr]
                        predecessors[t, curr] = prev
                    
                delta[t, curr] *= emissions[readings[t]][curr, curr]
            # Matrix.normalize(delta)
        Matrix.normalize(delta, axis=1)
        print(f"delta = {delta}")
                
        max_probability = 0
        path = [0] * len(readings)
        for step in range(self.total_positions):
            if max_probability < delta[len(readings) - 1, step]:
                max_probability = delta[len(readings) - 1, step]
                path[len(readings) - 1] = step
                
        print(f"pred = {predecessors}")
                
        for t in range(1, len(readings)):
            index = len(readings) - t
            path[index - 1] = predecessors[index, int(path[index])]
            
        paths_with_delta = []
            
        for i in range(len(path)):
            paths_with_delta.append(f"{i}: position = {int(path[i])}, probability = {delta[i, int(path[i])]}")
            
        # print(paths)
        
        delta_list = []
        print(delta)
        for step in delta:
            L = len(step)
            
            m = Matrix(L, 1)
            
            for index in range(len(step)):
                m[index, 0] = step[index]
                
            # print(m)
            
            delta_list.append(m)
            
        self.steps = delta_list
                
                
        return path, paths_with_delta
 
                                
    def print(self, filename, steps=None):
        """
            Print the maze and the probability of each position.
        """
        steps = self.steps if steps is None else steps
        
        # print(f"self.steps = {self.steps}")
        
        with open(filename, 'w') as f:
            s = ""
            for step in range(len(steps)):
                s += f"Step {step}\n"
                
                state = Matrix(self.maze.height, self.maze.width)
                for pos in range(0, steps[step].rows):
                    x, y = self.maze.de_index(pos)
                    state[y, x] = steps[step][pos, 0]
                
                s += str(state)
                s += "\n\n\n"
            f.write(s)
            print(s)
                
def test0():
    """
        Test the HMM on the first maze.
    """
    engine = HMM("./mazes/maze0.maz")
    engine.forward("RRRRRRRRRRRRRRRRRR")
    engine.print("output/maze0_f.out")
    engine.backward("RRRRRRRRRRRRRRRRRR")
    engine.print("output/maze0_b.out")
    engine.viterbi("RGRGRGRG")
                
def test1():
    """
        Test the HMM on the first maze.
    """
    engine = HMM("./mazes/maze1.maz")
    engine.forward("RGB")
    engine.print("maze1_f.out")
    engine.backward("BAC")
    engine.print("maze1_b.out")
    
def test2():
    engine = HMM("./mazes/maze1.maz")
    engine.forward("RGRG")
    engine.print("output/maze1_f.out")
    engine.backward("RGRG")
    engine.print("output/maze1_b.out")
    (paths, compounded) = engine.viterbi("RRGRRGRR")
    engine.print("output/maze1_viterbi.out")
    
    for item in compounded:
        print(item)
        
def test_viterbi():
    engine = HMM("./mazes/maze0.maz")
    (path, compounded) = engine.viterbi("RRGRRGRR")
    
    print(f"path found by viterbi algorithm: {path}")
    
    print(f"probability distributions. \
          NOTE: each row is a step in the")
    
    engine.print("output/maze1_viterbi.out")
    
    for item in compounded:
        print(item)
    

if __name__ == "__main__":
    test2()
    
    