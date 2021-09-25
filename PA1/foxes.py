#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""This file contains driver code for several Graph-search problems
    for the algorithms and data structures implemented in the other files in this directory.
"""
__author__ = "Amittai"
__copyright__ = "Copyright 2021"
__credits__ = ["Amittai", "Alberto Quattrini Li"]
__email__ = "Amittai.J.Wekesa.24@dartmouth.edu"
__github__ = "@siavava"

from FoxProblem import FoxProblem
from uninformed_search import bfs_search, dfs_search, ids_search

# Create a few test problems:
problem331 = FoxProblem((3, 3, 1))
problem541 = FoxProblem((5, 4, 1))
problem551 = FoxProblem((5, 5, 1))

# Run the searches.
#  Each of the search algorithms should return a SearchSolution object,
#  even if the goal was not found. If goal not found, len() of the path
#  in the solution object should be 0.

print(bfs_search(problem331))
print(dfs_search(problem331))
print(ids_search(problem331))
#
print(bfs_search(problem551))
print(dfs_search(problem551))
print(ids_search(problem551))

print(bfs_search(problem541))
print(dfs_search(problem541))
print(ids_search(problem541))

# testprob = FoxProblem((12, 10, 1))
# print(bfs_search(testprob))
# print(dfs_search(testprob))
# print(ids_search(testprob))
