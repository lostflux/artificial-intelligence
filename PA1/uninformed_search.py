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
    visited_states.add(search_problem.state)

    # While nodes are enqueued for visitation,
    while len(visit_queue) > 0:

        # get node at front of queue, add to visited set and visit it.
        current_node = visit_queue.popleft()
        solution.nodes_visited = solution.nodes_visited + 1
        visited_states.add(current_node.state)

        # If node is not goal state, get successors and enqueue them.
        if not search_problem.is_goal(current_node.state):
            for next_state in search_problem.get_successors(current_node.state):
                if next_state not in visited_states:
                    new_node = SearchNode(next_state, current_node)
                    visit_queue.append(new_node)
                    visited_states.add(new_node.state)

        # else, mark node as end-point and backtrack to find path.
        else:
            final_node = current_node
            while final_node is not None:
                solution.path.insert(0, final_node.state)
                final_node = final_node.parent
            break

    return solution


# Don't forget that your dfs function should be recursive and do path checking,
#  rather than memoizing (no visited set!) to be memory efficient

# We pass the solution along to each new recursive call to dfs_search
#  so that statistics like number of nodes visited or recursion depth
#  might be recorded
def dfs_search(search_problem, depth_limit=100, node=None, solution=None):
    # if no node object given, create a new search from starting state

    # start_state = search_problem.start_state
    if node is None:
        node = SearchNode(search_problem.start_state)
        solution = SearchSolution(search_problem, "DFS")

    # initialize the starting node's state, add to path, and increment number of visited nodes.
    current_state = node.state
    solution.path.append(current_state)
    solution.nodes_visited = solution.nodes_visited + 1

    # for each next state, if not yet visited and within search depth, recursively visit.
    for next_state in search_problem.get_successors(current_state):
        if depth_limit > 0 and next_state not in solution.path:
            next_node = SearchNode(next_state, node)
            dfs_search(search_problem, depth_limit=depth_limit-1, node=next_node, solution=solution)

    # If no fruitful path found, remove the state from the path.
    if not search_problem.is_goal(solution.path[-1]):
        solution.path.pop()

    # return final solution.
    return solution


def ids_search(search_problem, depth_limit=30):
    # 1. Initialize the start node and solution.
    start_node = SearchNode(search_problem.start_state)
    solution = SearchSolution(search_problem, "IDS")

    # 2. Iterate over depths, incrementing by 1 at each step.
    for current_depth in range(0, depth_limit):

        # 3. Do a DFS with the current depth.
        dfs_search(search_problem, node=start_node, solution=solution, depth_limit=current_depth)

        # 4. If the goal has been found, stop checking deeper depths (break the loop)
        if len(solution.path) > 0 and search_problem.is_goal(solution.path[-1]):
            break

        # 5. Or else... Reset the path (just to be safe!)
        else:
            solution.path = []

    # Return the final solution.
    return solution
