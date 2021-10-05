#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    This module implements functionality for a human Chess player.
"""
__author__ = "Amittai"
__copyright__ = "Copyright 2021"
__credits__ = ["Amittai"]
__email__ = "Amittai.J.Wekesa.24@dartmouth.edu"
__github__ = "@siavava"

import chess

class HumanPlayer():
    def __init__(self):
        print("Moves can be entered using four characters. For example, d2d4 moves the piece "
              "at d2 to d4.")
        pass

    def choose_move(self, board):
        moves = list(board.legal_moves)

        uci_move = None

        while not uci_move in moves:
            print("Please enter your move: ")
            human_move = input()

            try:
                uci_move = chess.Move.from_uci(human_move)
            except:
                # illegal move format
                uci_move = None

            if uci_move not in moves:
                print("  That is not a legal move!")


        print(uci_move in moves)

        return uci_move

