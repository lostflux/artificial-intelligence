
from collections import deque
from SearchSolution import SearchSolution
from FoxProblem import *

# you might find a SearchNode class useful to wrap state objects,
#  keep track of current depth for the dfs, and point to parent nodes
class SearchNode:
    # each search node except the root has a parent node
    # and all search nodes wrap a state object

    def __init__(self, state, parent=None):
        # you write this part
        self.state = state
        self.parent = parent

# you might write other helper functions, too. For example,
#  I like to separate out backchaining, and the dfs path checking functions


def bfs_search(search_problem: FoxProblem):

    solution = SearchSolution(search_problem, "BFS")

    visit_queue = deque()
    start_node = SearchNode(search_problem.state)
    visit_queue.append(start_node)


# Don't forget that your dfs function should be recursive and do path checking,
#  rather than memoizing (no visited set!) to be memory efficient

# We pass the solution along to each new recursive call to dfs_search
#  so that statistics like number of nodes visited or recursion depth
#  might be recorded
def dfs_search(search_problem, depth_limit=100, node=None, solution=None):
    # if no node object given, create a new search from starting state
    if node == None:
        node = SearchNode(search_problem.start_state)
        solution = SearchSolution(search_problem, "DFS")

    # you write this part



def ids_search(search_problem, depth_limit=100):
    # you write this part
    solution = SearchSolution(search_problem, "IDS")
