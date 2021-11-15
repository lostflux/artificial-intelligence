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
    """
        This class implements a solver for Hidden Markov Models.\n
        It's capable of locating a likely position for a robot in a Maze.\n
        With a little generalization it should be able to handle general\n
        Hidden Markov Model problems.\n
    """
    def __init__(self, filename):
        """
            Create a new HMM based on the given map file.
        """
        self.maze = Maze(filename)
        self.total_positions = self.maze.count_positions()
        self.valid_positions = self.maze.valid_positions()
        self.viterbi_path = None
        self.path_actual_data = None
        self.viterbi_info = None
        self.sensor_data = None
        if not self.total_positions:
            raise ValueError('No possible positions in maze.')
        
        # initialize matrices for sensor probabilities of detecting each color.
        
        # color -> probabilities of that color being read for each position in Maze        
        self.sensor_probabilities = {
            color: Matrix(self.total_positions, self.total_positions) for color in self.maze.colors
            }
            
        # initialize transition matrix for each position and adjacents.
        self.transitions = Matrix(self.total_positions, self.total_positions)
        
        # initialize initial distribution for robot location in Maze
        
        self.position_distribution = Matrix(self.total_positions, 1)
        
        # initialize list of steps in Mase -- used with algorithms.
        self.steps = []
        
        # call helper method to initialize variables.
        self.initialize_probabilities() 
        
    def initialize_probabilities(self):
        """
        Initializes the probabilities dictionary.
        """
        
        # iterate over all possible positions in Maze,
        for x in range(self.maze.width):
            for y in range(self.maze.height):
                
                # get character at position
                curr_char = self.maze.get_char(x, y)
                
                # if character means position is valid...
                if curr_char is not None and curr_char != '#':
                
                    # compute sensor detection probabilities
                    # (how likely is each color to be detected when on that square?)
                    self.compute_sensor_values(x, y, curr_char)
                    
                    # compute probabilities for next transition 
                    # (whether to stay put or move, and to where)
                    self.compute_transition_matrix(x, y, curr_char)
                    
                    # Since it's a valid position, there is some probability
                    # of robot starting on that position.
                    # Compute that probability -- (just 1 / total possible positions).
                    index = self.maze.index(x, y)
                    self.position_distribution[index, 0] = 1 / self.valid_positions
                
    def compute_sensor_values(self, x, y, c):
        """
            Compute the transition matrix for the given x, y position.\n
            NOTE: This is a helper method to `initialize_probabilities`.
        """
        pos = self.maze.index(x, y)
        for color in self.maze.colors:
            if color == c:
                self.sensor_probabilities[color][pos, pos] = CORRECT_COLOR
            else:
                self.sensor_probabilities[color][pos, pos] = WRONG_COLOR / (self.maze.color_count - 1)
   
    def compute_transition_matrix(self, x, y, c):
        """
            Return the transition matrix for the given x, y position.
        """
        
        current_index = self.maze.index(x, y)
        
        for dx, dy in zip([-1, 1, 0, 0], [0, 0, 1, -1]):
            cx, cy = x + dx, y + dy
            c = self.maze.get_char(cx, cy)
            if c is not None and c != '#':
                next_index = self.maze.index(cx, cy)
                self.transitions[current_index, next_index] = MOVE_PROBABILITY
            else:
                self.transitions[current_index, current_index] = MOVE_PROBABILITY
                
        
    def compute_distribution(self, x, y, total):
        """
            Compute the distribution for the given x, y position.
        """
        if self.maze.get_char(x, y) != '#':
            self.position_distribution[x, y] = 1 / total
            
    def forward(self, readings: str):
        
        readings = readings.lower()
        self.sensor_data = readings
        
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
            distribution = self.sensor_probabilities[reading] * (self.transitions.transpose() * distribution)
            
            Matrix.normalize(distribution)
            
            self.steps.append(distribution)
            
            
            
    def backward(self, readings: str):
        """
            Compute the probability of the robot ending up in each position
            after the given readings.
        """
        readings = readings.lower()
        self.sensor_data = readings
        
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
        
        # normalize readings -- lower or upercase doesn't matter.
        readings = readings.lower()
        self.sensor_data = readings
        
        # get transition matrix
        T = self.transitions
        
        # get emission matrices
        emissions = self.sensor_probabilities
        
        # get initial distribution
        IP = self.position_distribution 
        
        
        # Initialization
        delta = Matrix.zeros(len(readings), self.total_positions)
        predecessors = Matrix.copy(delta)
        for pos in range(self.total_positions):
            delta[0, pos] = IP[pos, 0] * T[pos, pos]
            
        # Dynamic Programming step.
        # NOTE: 
        #   1. t -> time
        #   2. c -> current
        #   3. p -> previous
        for t in range(1, len(readings)):
            for c in range(self.total_positions):
                for p in range(self.total_positions):
                    if delta[t, c] < delta[t-1, p] * T[p, c]:
                        delta[t, c] = delta[t-1, p] * T[p, c]
                        predecessors[t, c] = p
                    
                delta[t, c] *= emissions[readings[t]][c, c]
        Matrix.normalize(delta, axis=1)
                
        # backtrack to find the most likely 
        # states for each time step.
        # and rebuild actual path
        max_probability = 0
        path = [0] * len(readings)
        for pos in range(self.total_positions):
            if max_probability < delta[len(readings) - 1, pos]:
                max_probability = delta[len(readings) - 1, pos]
                path[len(readings) - 1] = pos
        for t in range(1, len(readings)):
            index = len(readings) - t
            path[index - 1] = predecessors[index, int(path[index])]
                

            
        # just an array to show useful information.
        compounded = []
        for i in range(len(path)):
            s = f"t = {i}: loc = {int(path[i])}, prob = {delta[i, int(path[i])]}"
            compounded.append(s)
            
        
        delta_list = []
        for step in delta:
            L = len(step)
            
            m = Matrix(L, 1)
            
            for index in range(len(step)):
                m[index, 0] = step[index]
            
            delta_list.append(m)
        
        # save probabilities, path, and info to HMM
        self.steps = delta_list
        self.viterbi_path = [self.maze.de_index(x) for x in path]
        self.path_actual_data = [self.maze.get_char(x, y) for (x, y) in self.viterbi_path]
        self.viterbi_info = compounded
 
                                
    def print(self, filename, steps=None):
        """
            Print the maze and the probability of each position.
        """
        steps = self.steps if steps is None else steps
        
        
        with open(filename, 'w') as f:
            s = f"sensor readings = {self.sensor_data}\n\n"
            
            if self.viterbi_path:
                s += f"Viterbi path: {self.viterbi_path}\n"
                s += f"Actual values on map: {self.path_actual_data}\n"
                for info in self.viterbi_info:
                    s += f"{info}\n"
                s += f"\n\n"
            
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
                
def test(filename, observations: str):
    """
        Test the HMM on the first maze.
    """
    basename = filename.split("/")[-1].split(".")[0]
    
    forward = f"output/{basename}.forward"
    backward = f"output/{basename}.backward"
    viterbi = f"output/{basename}.viterbi"
    
    engine = HMM(filename)
    engine.forward(observations)
    engine.print(forward)
    engine.backward(observations)
    engine.print(backward)
    engine.viterbi(observations)
    engine.print(viterbi)
    

def test0():
    """
        Test the HMM on the first maze.
    """
    
    test("./mazes/maze0.maz", "RGBGPQ")
                
def test1():
    """
        Test the HMM on the first maze.
    """
    
    test("./mazes/maze1.maz", "RGB")
    
def test2():
    """
        Test the HMM on the first maze.
    """
    
    test("./mazes/maze2.maz", "RGB")
    
def test5():
    """
        Test the HMM on maze 5.
    """
    
    test("./mazes/maze5.maz", "POMONACOLLEGE")
    
def test3():
    """
        Test the HMM on the first maze.
    """
    
    test("./mazes/maze3.maz", "ABCDEFGHIJK")
    
def test4():
    """
        Test the HMM on the first maze.
    """
    
    test("./mazes/maze4.maz", "ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    
def test_text():
    """
        Test HMM on map file with comprehensible text.
    """
    test("./mazes/text.maz", "temporalprobabilisticmodel")
    
    

if __name__ == "__main__":
    
    test0()
    test1()
    test3()
    test4()
    test5()
    # test_text() # This takes some time but should finish in about a minute.
    
    