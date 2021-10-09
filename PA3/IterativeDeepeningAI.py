#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""This file implements several algorithms for intelligent gameplay, including Miniman AI.
"""
__author__ = "Amittai"
__copyright__ = "Copyright 2021"
__credits__ = ["Amittai"]
__email__ = "Amittai.J.Wekesa.24@dartmouth.edu"
__github__ = "@siavava"

from numpy import inf                               # infinity
from chess import Board                             # Chess board
import chess                                        # Chess module
from TranspositionTable import TranspositionTable
from random import shuffle

from MinimaxAI import MinimaxAI

class IterativeDeepeningAI(MinimaxAI):
    
    
    def __init__(self, max_depth=5, maximizing=True, debug=True):
        self.max_depth = max_depth
        self.debug = debug
        self.memory: TranspositionTable = TranspositionTable()
        self.search_engine: MinimaxAI = MinimaxAI(0, debug=debug)
        
       
     
    def choose_move(self, board: Board):
        """
            Given a board state, chooses the best move to play next.
        """
        
        # get all moves, initialize best utility to neg infinity.
        # best_move = None
        # best_value = -inf if self.maximizing else inf
        # all_moves = list(board.legal_moves)
        # shuffle(all_moves)
        
        # check every move and remember the last move that improves the utility.
        best_move, best_cost = None, -inf
        for depth in range(2, self.max_depth):
            
            move = self.search_engine.choose_move(board, depth=depth)
            
            board.push(move)
            cost = self.memory[board]
            board.pop()
            
            if cost > best_cost:
                best_cost = cost
                best_move = move
            
            print(f"Depth {depth}: Best Move = {best_move}, cost = {best_cost}")
            
        return best_move
    #     for move in all_moves:
            
    #         board.push(move)
    #         if board in self.seen_states:
    #             score = self.seen_states[str(board)]
            
    #         else:
    #             score = self.minimax(board)
                
    #             #########! if debug flag is set, print debug info. #########
    #             if self.debug:
    #                 print(f"move = {move}, minimax = {score}")
    #             self.seen_states[board] = score
                
                
                
    #         if self.maximizing and (score > best_value):
    #             best_move = move
    #             best_value = score
                
    #             if best_value == inf:
    #                 break
                
    #         elif score <= best_value:
    #             best_move = move
    #             best_value = score
                
    #             if best_value == -inf:
    #                 break
            
    #         board.pop()
        
    #     ######### if debug flag is set, print debug info. #########
    #     if self.debug:
    #         print(f"Transposition Table size: {len(self.seen_states)}")
            
    #     print("Minimax AI recommending move " + str(best_move))
    #     return best_move
        
    
    # def ids_search(search_problem, depth_limit=30):
    #     """This method runs IDS -- Iterative Deepening Search on the implicit Graph
    #     underlying a specified search  problem and start state.
    #         :arg search_problem: a FoxProblem instance.
    #         :arg depth_limit: integer specifying maximum search depth. Defaults to 0.
    #         :return solution: a SearchSolution instance carrying information about the search run.
    #     """
    #     # 1. Initialize the start node and solution.
    #     start_node = SearchNode(search_problem.start_state)
    #     solution = SearchSolution(search_problem, "IDS")

    #     # 2. Iterate over depths, incrementing by 1 at each step.
    #     for current_depth in range(0, depth_limit):

    #         # 3. Do a DFS with the current depth.
    #         dfs_search(search_problem, node=start_node, solution=solution, depth_limit=current_depth)

    #         # 4. If the goal has been found, stop checking deeper depths (break the loop)
    #         if len(solution.path) > 0 and search_problem.is_goal(solution.path[-1]):
    #             break

    #         # 5. Or else... Reset the path (just to be safe!)
    #         else:
    #             solution.path = []

    #     # Return the final solution.
    #     return solution