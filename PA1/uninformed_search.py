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

    start_node = SearchNode(search_problem.state)
    visit_queue = deque()
    visit_queue.append(start_node)

    visited_states = set()

    final_node = None

    while len(visit_queue) > 0:
        current_node = visit_queue.popleft()
        if not search_problem.is_goal(current_node.state):
            for next_state in search_problem.get_successors(current_node.state):
                if next_state not in visited_states:
                    new_node = SearchNode(next_state, current_node)
                    visit_queue.append(new_node)
                    visited_states.add(next_state)
        else:
            final_node = current_node
            break

    if final_node is None:
        solution.path = "No path was found."
    else:
        while final_node is not None:
            solution.path.insert(0, final_node.state)
            final_node = final_node.parent

    return solution.path


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
    current_state = search_problem.start_state
    for next_state in search_problem.get_successors(current_state):
        dfs_search(search_problem, next_state, node)


def ids_search(search_problem, depth_limit=100):
    # you write this part
    solution = SearchSolution(search_problem, "IDS")
