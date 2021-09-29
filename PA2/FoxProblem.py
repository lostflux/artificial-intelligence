#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""This module implements a data structure and associated methods for modelling Chicken - and - Foxes problems.
"""
__author__ = "Amittai"
__copyright__ = "Copyright 2021"
__credits__ = ["Amittai", "Alberto Quattrini Li"]
__email__ = "Amittai.J.Wekesa.24@dartmouth.edu"
__github__ = "@siavava"


class FoxProblem:
    def __init__(self, start_state=(3, 3, 1)):
        self.start_state = start_state
        self.goal_state = (0, 0, 0)
        self.state = start_state
        self.total_chickens = start_state[0]
        self.total_foxes = start_state[1]
        self.boat_ashore = bool(start_state[2])

        # you might want to add other things to the problem,
        #  like the total number of chickens (which you can figure out
        #  based on start_state

    # get successor states for the given state
    def get_successors(self, state):
        
        # initialize set of next states.
        next_states = set()
        
        # iterate over all possible chickens and foxes leaving.
        for num_chickens in range(0, 3):
            for num_foxes in range(0, 3):
                
                # check the total animals leaving.
                # It should not be greater than the size of the boat.
                total = num_chickens + num_foxes
                if 1 <= total <= 2:  # ignore states the empty transition

                    # check if the boat is leaving side A or B.
                    if state[2] == 1:
                        # BOAT LEAVING side A
                        new_chickens = state[0] - num_chickens  # find new number of chicken ashore
                        new_foxes = state[1] - num_foxes  # find new number of foxes ashore
                        next_state = (new_chickens, new_foxes, 0)

                        # check the state for validity, append to valid states
                        if self.is_valid(next_state):
                            # print("2", next_state)
                            next_states.add(next_state)

                    elif state[2] == 0:
                        # BOAT RETURNING TO SIDE A
                        new_chickens = state[0] + num_chickens  # find new number of chicken ashore
                        new_foxes = state[1] + num_foxes  # find new number of foxes ashore
                        next_state = (new_chickens, new_foxes, 1)

                        # check the state for validity, append to valid states
                        if self.is_valid(next_state):
                            next_states.add(next_state)
                            
        # return compiled set of states
        return next_states

    # I also had a goal test method. You should write one.
    def is_goal(self, state):
        return self.goal_state == state

    def is_valid(self, state):

        # A valid state cannot have negative chickens / foxes
        if state[0] < 0 or state[1] < 0:
            return False

        new_chicken_count = state[0]
        chickens_side_B = self.total_chickens - new_chicken_count

        new_fox_count = state[1]
        foxes_side_B = self.total_foxes - new_fox_count

        # 1, make sure proposed move is within bounds of how many chickens and foxes are available.
        if new_chicken_count <= self.total_chickens and new_fox_count <= self.total_foxes:

            # 2, if chickens >= foxes on both sides of the bank, move is valid.
            if new_chicken_count >= new_fox_count and chickens_side_B >= foxes_side_B:
                return True

            # 3, otherwise, if there are more foxes on a bank that has 0 chickens, move is valid.
            elif new_chicken_count < new_fox_count and new_chicken_count == 0:
                return True
            elif chickens_side_B < foxes_side_B and chickens_side_B == 0:
                return True

        # 4 move is invalid
        return False

    def __str__(self):
        string = "Chickens and foxes problem: " + str(self.start_state)
        return string

# A bit of test code


def check_states(state, goal_state):
    if state == goal_state:
        print("Found!")
        return

    print(test_cp.get_successors(state))
    for n_state in test_cp.get_successors(state):
        check_states(n_state, goal_state)


if __name__ == "__main__":
    test_cp = FoxProblem((5, 5, 1))
    print(test_cp.get_successors((5, 5, 1)))
    start_state = (5, 5, 1)
    goal_state = (0, 0, 0)
    check_states(start_state, goal_state)
    # while True:

    print(test_cp)

# Note: I used these loops to hunt for a path to the solution for the (3, 3, 1) search problem using brute force.

    # To test next states
    # start_state = (3, 3, 1)
    # test2 = FoxProblem(start_state)
    # print(test2.get_successors((0, 3, 1)))
    # for n_state in test2.get_successors(start_state):
    #     for next_state_2 in test2.get_successors(n_state):
    #         for next_state_3 in test2.get_successors(next_state_2):
    #             for next_state_4 in test2.get_successors(next_state_3):
    #                 print(f"{start_state} "
    #                       f"-> {n_state} "
    #                       f"-> {next_state_2} "
    #                       f"-> {next_state_3} "
    #                       f"-> {next_state_4} "
    #                       f"-> {test2.get_successors(next_state_4)}")
    # print(test2.get_successors((3, 3, 1)))
