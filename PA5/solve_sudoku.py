#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Run a test-run to solve a Sudoku problem.
"""
__author__ = "Amittai"
__copyright__ = "Copyright 2021"
__credits__ = ["Amittai", "Alberto Quattrini Li"]
__email__ = "Amittai.J.Wekesa.24@dartmouth.edu"
__github__ = "@siavava"

from display import display_sudoku_solution
import random, sys
from SAT import SAT


import cProfile, pstats, io
from pstats import SortKey

def test_gsat():
    # for testing, always initialize the pseudorandom number generator to output the same sequence
    #  of values:
    random.seed(1)
    
    print(sys.argv)

    puzzle_name = str(sys.argv[1][:-4])
    sol_filename = puzzle_name + ".sol"

    sat = SAT(sys.argv[1])

    result = sat.gsat()

    if result:
        sat.write_solution(sol_filename)
        display_sudoku_solution(sol_filename)
        
def test_walksat():
    # for testing, always initialize the pseudorandom number generator to output the same sequence
    #  of values:
    random.seed(1)
    
    print(sys.argv)

    puzzle_name = str(sys.argv[1][:-4])
    sol_filename = puzzle_name + ".sol"

    sat = SAT(sys.argv[1])

    result = sat.walksat()

    if result:
        sat.write_solution(sol_filename)
        display_sudoku_solution(sol_filename)

if __name__ == "__main__":
    
# Start profiling.
    pr = cProfile.Profile()
    pr.enable()
    
    # search using gsat
    test_gsat()
    
    # search using walksat
    # test_walksat()
    
# Stop profiling and print stats.
    pr.disable()
    s = io.StringIO()
    sortby = SortKey.CUMULATIVE
    ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
    ps.print_stats()
    print(s.getvalue())