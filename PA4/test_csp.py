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

from CSP import CSP
from backtracking import backtracking_search

from erratum import (log_error, log_info, log_debug_info)

def test1():
    """
        This function tests the backtracking algorithm.
    """
    # Create a CSP
    
    variables: set = {"Amittai", "Alphonso", "Fabricio"}
    domains: dict = {"Amittai": {1, 3}, "Alphonso": {2, 3}, "Fabricio": {4, 3}}
    constraints: set = { ("Amittai", "Alphonso"), ("Amittai", "Fabricio"), ("Alphonso", "Fabricio")}
    
    csp = CSP(variables=variables, domains=domains, constraints=constraints, debug=True)
    
    results = backtracking_search(csp)
    
    log_info(results)
    
    log_error(csp)
    
    
    
    # csp.add_variable('A', [1, 2, 3])
    
if __name__ == "__main__":
    test1()