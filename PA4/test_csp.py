#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    This file implements test routines for CSP algorithms.
"""
__author__ = "Amittai"
__copyright__ = "Copyright 2021"
__credits__ = ["Amittai"]
__email__ = "Amittai.J.Wekesa.24@dartmouth.edu"
__github__ = "@siavava"

from numpy import inf

from CSP import CSP

from CircuitProblem import CircuitProblem

from backtracking import backtracking_search

from erratum import (log_error, log_info, log_debug_info)

import cProfile, pstats, io
from pstats import SortKey

def test1():
    """
        This function tests the backtracking algorithm with a simple CSP based on my roommates and I.
    """
    # Create a CSP
    
    variables: set = {"Amittai", "Alphonso", "Fabricio"}
    domains: dict = {"Alphonso": {1, 2, 3}, "Amittai": {1},  "Fabricio": {1, 2}}
    constraints: set = { ("Amittai", "Alphonso"), ("Amittai", "Fabricio"), ("Alphonso", "Fabricio")}
    
    csp = CSP(variables=variables, domains=domains, constraints=constraints, mrv=True, lcv=True, debug=True)
    
    results = backtracking_search(csp)
    
    log_info(f"\n\nfinal assignments: {results}")
    
    log_info(csp)
    
def test2():
    """
        This function tests the backtracking algorithm with a simple CSP based on my roommates and I.
    """
    # Create a CSP
    
    variables: set = {"Amittai", "Alphonso", "Fabricio"}
    domains: dict = {"Alphonso": {1, 2, 3}, "Amittai": {1},  "Fabricio": {1, 2}}
    constraints: set = { ("Amittai", "Alphonso"), ("Amittai", "Fabricio"), ("Alphonso", "Fabricio")}
    
    csp = CSP(variables=variables, domains=domains, constraints=constraints, mrv=True, lcv=True, debug=True)
    
    results = backtracking_search(csp, inference=True)
    
    log_info(f"\n\nfinal assignments: {results}")
    
    log_info(csp)

def test3():
    """
        This function tests the backtracking algorithm with a simple CSP based on my roommates and I.
    """
    # Create a CSP
    
    variables: set = {"WA", "NT", "Q", "NSW", "V", "SA", "T"}
    domains: dict = {"WA": {"R"}, "NT" : {"R", "G", "B"}, "Q" : {"R", "G", "B"},\
        "NSW" : {"R", "G", "B"}, "V" : {"R", "G", "B"}, "SA" : {"R", "G", "B"}, "T" : {"R", "G", "B"}}
    constraints: set = { 
                            ("WA", "NT"), ("WA", "SA"), ("SA", "NT"),\
                            ("Q", "NSW"), ("SA", "Q"), ("NT", "Q"),\
                            ("SA", "NSW"), ("SA", "V"), ("NSW", "V")
                        }
    
    csp = CSP(variables=variables, domains=domains, constraints=constraints, mrv=True, lcv=True, debug=True)
    
    results = backtracking_search(csp)
    
    log_info(csp.display(results))
    
    log_info(f"\n\nfinal assignments: {results}")
    
    log_info(csp)
    
def test4():
    """
        This function tests the backtracking algorithm with a simple CSP based on my roommates and I.
    """
    # Create a CSP
    
    variables: set = {("a", 3, 2), ("b", 5, 2), ("c", 2, 3), ("e", 7, 1)}
    # variables: set = {("a", 3, 1)}
    csp: CircuitProblem = CircuitProblem(10, 3, variables=variables, debug=True)
    
    results = backtracking_search(csp, inference=True)
    
    log_info(f"\n\nfinal assignments: {results}")
    
    log_info(csp.display(results))
    
    
if __name__ == "__main__":
    
    pr = cProfile.Profile()
    pr.enable()
    
    
    # test1()
    # test2()
    # test3()
    test4()
    
    pr.disable()
    s = io.StringIO()
    sortby = SortKey.CUMULATIVE
    ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
    ps.print_stats()
    print(s.getvalue())