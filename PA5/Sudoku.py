#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    This file implements functionality for representing a Sudoku game.
    
"""
__author__ = "Amittai"
__copyright__ = "Copyright 2021"
__credits__ = ["Amittai", "Alberto Quattrini Li"]
__email__ = "Amittai.J.Wekesa.24@dartmouth.edu"
__github__ = "@siavava"

from erratum import (log_error, log_info, log_debug_info )   # logging functions. see [./erratum.py]

class Sudoku:
    def __init__(self):
        """
            A new Sudoku game with all cells unassigned (set to ZERO).
        """
        
        # initialize all cells to 0
        self.numbers = [[0 for i in range(9)] for j in range(9)]

    def load(self, filename):
        """
            Loads a Sudoku game from a file.
            NOTE: If error reading file, raise Exception.
        """
        try:
            with open(filename, "r") as f:
                r = 1
                for line in f:
                    c = 1
                    # each line contains a row
                    for s in line.split():
                        self.set(r, c, int(s))
                        c += 1

                    r += 1
                log_info("Loaded Sudoku from file: " + filename)
            
        except IOError as err:
            log_error("Could not load Sudoku from file: " + filename)
            raise IOError(err)

    def get(self, r, c):
        """
            Get value at specified position in Sudoku.
            NOTE: Sudoku positions are 1-indexed.
        """
        return self.numbers[r - 1][c - 1]

    def set(self, r, c, value):
        """
            Set value at specified position in Sudoku.
            NOTE: Sudoku positions are 1-indexed.
        """
        
        try:
            self.numbers[r - 1][c - 1] = value
        except IndexError:
            log_error("Invalid Sudoku position: " + str(r) + "," + str(c) + "," + str(value))

    def read_solution(self, filename):
        """
            Load Sudoku solution from a file.
            
        """
        try:
            with open(filename, "r") as f:
                for line in f:
                    # ignore unset variables
                    literal = int(line)
                    if literal > 0:
                        r = int(line[0])
                        c = int(line[1])
                        v = int(line[2])
                        self.set(r, c, v)
                f.close()
                log_info("Loaded Sudoku solution from file: " + filename)
                
        except IOError as err:
            log_error("Could not load Sudoku solution from file: " + filename)
            raise IOError(err)
        
    def write_solution(self, filename):
        """
            Write Sudoku solution to a file.
        """
        with open(filename, "w") as f:
            for r in range(1, 10):
                for c in range(1, 10):
                    v = self.get(r, c)
                    if v != 0:
                        f.write(str(r) + str(c) + str(v) + "\n")

            f.close()
            log_info(f"Sudoku solution written to file: {filename}")

    def __str__(self):
        """
            Generate stringified value of Sudoku.
        """
        s = ""
        for r in range(1, 10):
            if r == 4 or r == 7:
                s += "---------------------\n"

            for c in range(1, 10):

                if c == 4 or c == 7:
                    s += "| "
                s = s + str(self.get(r, c))
                s += " "

            s += "\n"

        return s

    def sudoku_literal(self, r, c, v, neg=False):
        return ("-" if neg else "") + str(r) + str(c) + str(v)

    def cell_clause(self, r, c):

        s = ""

        # at least one value:
        atleastone_str = ""
        for value in range(1, 10):
            atleastone_str += self.sudoku_literal(r, c, value) + " "
        atleastone_str += " \n"

        s = atleastone_str

        for vi in range(1, 10):
            for vj in range(vi + 1, 10):
                s += self.sudoku_literal(r, c, vi, neg=True) + " "
                s += self.sudoku_literal(r, c, vj, neg=True) + " "
                s += "\n"

        return s

    def row_clause(self, r):
        s = ""
        for value in range(1, 10):
            for c in range(1, 10):
                s += self.sudoku_literal(r, c, value) + " "
            s += "\n"

        return s

    def col_clause(self, c):
        s = ""
        for value in range(1, 10):
            for r in range(1, 10):
                s += self.sudoku_literal(r, c, value) + " "
            s += "\n"

        return s

    def write_block_clauses(self, filehandle):

        s = ""

        for sr in range(1, 10, 3):
            for sc in range(1, 10, 3):
                for value in range(1, 10):
                    for r_offset in range(3):
                        for c_offset in range(3):
                            r = sr + r_offset
                            c = sc + c_offset
                            s += self.sudoku_literal(r, c, value) + " "

                    s += "\n"

        filehandle.write(s)

    def write_fixed_clauses(self, filehandle):
        s = ""
        for r in range(1, 10):
            for c in range(1, 10):
                value = self.get(r, c)
                if value !=  0:
                    s += self.sudoku_literal(r, c, value) + "\n"

        filehandle.write(s)


    def write_col_clauses(self, filehandle):
        for c in range(1, 10):
            clause = self.col_clause(c)
            filehandle.write(clause)


    def write_row_clauses(self, filehandle):
        for r in range(1, 10):
            clause = self.row_clause(r)
            filehandle.write(clause)

    def write_cell_clauses(self, filehandle):
        for r in range(1, 10):
            for c in range(1, 10):
                clause = self.cell_clause(r, c)
                filehandle.write(clause)

    def generate_cnf(self, filename):
        """
            Geenrate the Conjunctive Normal Form (CNF) of the Sudoku.
        """
        try:
            with open(filename, "w") as f:
                self.write_cell_clauses(f)
                self.write_row_clauses(f)
                self.write_col_clauses(f)
                self.write_block_clauses(f)
                self.write_fixed_clauses(f)
                f.close()
                log_info("Generated CNF file: " + filename)
        except IOError as err:
            log_error("Could not generate CNF file: " + filename)
            raise IOError(err)


if __name__ == "__main__":
    test_sudoku = Sudoku()

    test_sudoku.load("puzzle1.sud")
    #print(test_sudoku)
    # print(sudoku_literal(2, 3, 9, neg=True))

    # print(cell_clause(1, 1))

    test_sudoku.generate_cnf("puzzle1.cnf")

    #test_sudoku.read_solution("rules.sol")
    print(test_sudoku)
