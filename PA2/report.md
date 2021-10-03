# COSC 76: Artificial Intelligence

## Programming Assignment 2: Mazeworld

### Student: Amittai Wekesa (github: @siavava)

### Winter 2021

$k$ robots live in an $n$ x $n$ rectangular maze. The coordinates of each robot are $(x_i, y_i)$, and each coordinate is an integer in the range $0...n-1$. For example, maybe the maze looks like this:

```text
. B . . . . .
. # # . C . .
. . # # . . .
. . . . # . .
. . # # . . .
. . # . . . .
A . . . # # .
```

That's three robots $A$, $B$, $C$ in a 7x7 maze. You'd like to get the robots to another configuration. For example:

```text
. . . . . . .
. # # . . . .
. . # # . . .
. . . . # . .
. . # # . . B
. . # . . . A
. . . . # # C
```

There are some rules. The robots only move in four directions, north, south, east, and west. The robots cannot pass through each other, and may not occupy the same square. The robots move one at a time. First robot $A$ moves, then robot $B$, then robot $C$, then $D$, $E$, and eventually, $A$ gets another turn. Any robot may decide to give up its turn and not move. So there are five possible actions from any state.

Let's make the cost function the total fuel expended by the robots. A robot expends $1$ unit of fuel if it moves, and no fuel if it waits a turn.

Only one robot may occupy one square at a time. You are given a map ahead of time, and it will not change during the course of the game.

#### Discussion Questions (Mazeworld)

1. If there are $k$ robots, how would you represent the state of the system? Hint -- how many numbers are needed to exactly reconstruct the locations of all the robots, if we somehow forgot where all of the robots were? Further hint. Do you need to know anything else to determine exactly what actions are available from this state?

  > Given $k$ robots, we first have to know their exact locations. We can store this as either an array or struct carrying location information for each robot. Here, we can either make sure each robot's location coordinates remain in a certain index in the array (for instance, by using an immutable tuple) or use a dictionary to associate each robot with location. In total, we would need $2k$ numbers to be able to place each of the $k$ robots in exact $x$ and $y$ position.
  > We further need to know a robot's immediate surroundings to determine possible movements, but these can be inferred from the map data.
  > We also need to consider other robot locations so robots don't run into each other.

2. Give an upper bound on the number of states in the system, in terms of n and k.
  
  > Suppose the maze does not have walls, then there are $n^{2}$ possible position in the maze. Since the bots cannot collide (i.e. be in the same position at the same time), the first of the $k$ robots will have $n^{2}$ possible spots, the second will have $n^{2}-1$ possible spots, and the $k$'th robot will have $n^{2}-k$ possible locations. This sums up to a possible total of $\frac{n^{2}!}{k!}$ possible states.

3. Give a rough estimate on how many of these states represent collisions if the number of wall squares is w, and n is much larger than k.
  
  > Given that $w$ positions are walls, the number of possible positions reduces from $n^{2}$ to $n^{2}-w$. Thus, possible states without collissions will reduce to $\frac{(n^{2}-w)!}{k!}$. Thus, the number of collission states will be the difference: $\frac{n^{2}!}{k!}$ $-$ $\frac{(n^{2}-w)!}{k!}$

4. If there are not many walls, n is large (say 100x100), and several  robots (say 10), do you expect a straightforward breadth-first search on the state space to be computationally feasible for all start and goal pairs? Why or why not?

  > No, I do not expect a straightforward **BFS** to be able to find the path in reasonable time because, at that scale, the maze will have about $\frac{100!}{10!}$ possible states to check, which is a lot to search using an uninformed algorithm.

5. Describe a useful, monotonic heuristic function for this search space. Show that your heuristic is monotonic. See the textbook for a formal definition of monotonic.
It may seem that you can just plan paths for the robots independently using three different breadth-first-searches, but this approach won't work very well if the robots get close to one another or have to move around one another. Therefore, you should plan paths in the complete state space for the system.

  > In the 2D space, finding the Manhattan distance between points is a better heuristic than using direct distance, since diagonal movement is not permitted. If obstacles do exist, then the robot will be forced to take detours which results in a longer path. The **Manhattan distance** will be the shortest distance attainable between any two points in the maze.

6. Describe why the 8-puzzle in the book is a special case of this problem. Is the heuristic function you chose a good one for the 8-puzzle?

  > The 8-puzzel problem is akin to a special version of the Mazeworld problem. In the 8-puzzle problem, only one number (corrollary to robot) can move at a time. Similarly, numbers can only be moved in a directikon with an empty adjacent square. The catch is that in the 8-puzzle problem numbers are closer together and at any time only a maximum of 4 numbers can move, and each can only move in a single direction. The goal is also to get to a specific configuration/arrangement. The same can be interprated as moving the empty cell around in either of the four (up, down, left, right) directions, each time replacing it with whatever number is on the desired direction, until the numbers give a specific arrangement. The heuristic function used in `Mazeworld` is not necessarily a good one because numbers might need to be 

7. The state space of the 8-puzzle is made of two disjoint sets.  Describe how you would modify your program to prove this. (You do not have to implement this.)
  
  > Suppose the number of total inversions (larger numbers occurring before smaller numbers in the game) is $N$. The 8-puzzle game maintains the game that every move made must not change the value of $N$ `mod` 2. Because the solution has zero inversions (i.e. all the numbers are in order), then only puzzles from a starting state with $N$ `mod` $2 = 0$ can be solved.
  > To modify the Mazeworld problem, check the starting state of every puzzle and ascertain that they have an even number of inversions. Any puzzle with an odd number of inversions is unsolvable, so don't waste time trying it.


#### Discussion Questions (Blind Robot)

1. Describe what heuristic you used for the A* search. Is the heuristic optimistic? Are there other heuristics you might use? (An excellent might compare a few different heuristics for effectiveness and make an argument about optimality.)

  > For the Sensorless robot, my first intuition was to find the shortest Manhattan distance between two robots in any state, but I quickly realized that the strategy would return $0$ as soon as any two robots converged, and the strategy would crumble into another version of uninformed search.
  > The other ideas I had was to either use the closest pair that's nonzero or the farthest pair. Of these, the farthest pair worked better. I then tried finding the smallest reactangle that contains the robots then finding the Manhattan distance using the length and width of that square. This ultimately gave the best results of the three methods.

##### Implementation of closest neighbor's Manhattan distance

```python
    def manhattan_closest(self, state):
        """
            Given a state, return the shortest Manhattan distance between any two robots in the state.
        """
        
        closest = 2**20
        
        # For each robot, loop over every other robot in the maze, 
        # find the manhattan distance between them, 
        # and return the minimum of all such distances.
        for ix in range(0, len(state), 2):
            for jx in range(0, len(state), 2):
                if ix == jx:
                    continue
                
                dist = abs(state[ix]-state[jx]) + abs(state[ix+1]-state[jx+1])
                
                if dist != 0:
                    closest = min(closest, dist)
                
        return closest
```

###### Test results for closest pair

```text
----
Blind robot problem: Possible start locations: (1, 1, 13, 1, 1, 13, 13, 13)
Maze:
###############
#C...........D#
#.............#
#.............#
#.............#
#.............#
#.............#
#.............#
#.............#
#.............#
#.............#
#.............#
#.............#
#A...........B#
###############


attempted with search method Astar with heuristic manhattan_closest
number of nodes visited: 8113
solution length: 25
cost: 24
path: ...

Directions to take:
['N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'N', 'E']
Final position = (13, 13)
```

##### Implementation of farthest neighbor's Manhattan distance

```python
    def manhattan_farthest(self, state):
        """
            Given a state, return the farthest distance between any two robots in the state.
        """
        
        farthest = 0
        
        # For each robot, loop over every other robot in the maze, 
        # find the manhattan distance between them, 
        # and return the maximum of all such distances.
        for ix in range(0, len(state), 2):
            for jx in range(0, len(state), 2):
                if ix == jx:
                    continue
                
                dist = abs(state[ix]-state[jx]) + abs(state[ix+1]-state[jx+1])
                if dist != 0:
                    farthest = max(farthest, dist)
                
        return farthest
```

###### Test results for farthest pair

```text
----
Blind robot problem: Possible start locations: (1, 1, 13, 1, 1, 13, 13, 13)
Maze:
###############
#C...........D#
#.............#
#.............#
#.............#
#.............#
#.............#
#.............#
#.............#
#.............#
#.............#
#.............#
#.............#
#A...........B#
###############


attempted with search method Astar with heuristic manhattan_farthest
number of nodes visited: 119
solution length: 25
cost: 24
path: ...

Directions to take:
['N', 'N', 'N', 'N', 'E', 'N', 'N', 'E', 'N', 'N', 'N', 'N', 'E', 'E', 'N', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'N']
Final position = (13, 13)
```

##### Implementation of largest containing square's Manhattan distance

```python
    def manhattan_heuristic(self, state):
        """
            Calculate the manhattan distance for the set of bots using the max and min x and y coordinates.
        """
        
        # rather than using the normal Manhattan distance, box in all the robots
        # by finding the max and min coordinates in either both directions 
        # then using those to calculate the heuristic.
        max_x, max_y = 0, 0
        min_x, min_y = 0, 0
        
        for i in range(0, len(state), 2):
            ix, iy = i, i+1
            max_x = max(max_x, state[ix])
            min_x = min(min_x, state[ix])
            
            max_y = max(max_y, state[iy])
            min_y = min(min_y, state[iy])
                
        return abs(max_x - min_x) + abs(max_y - min_y)
```

###### Test results for containing rectangle

```text
----
Blind robot problem: Possible start locations: (1, 1, 13, 1, 1, 13, 13, 13)
Maze:
###############
#C...........D#
#.............#
#.............#
#.............#
#.............#
#.............#
#.............#
#.............#
#.............#
#.............#
#.............#
#.............#
#A...........B#
###############


attempted with search method Astar with heuristic manhattan_heuristic
number of nodes visited: 107
solution length: 25
cost: 24
path: ...

Directions to take:
['W', 'W', 'W', 'W', 'W', 'S', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S']
Final position = (1, 1)
```

#### TL;DR

1. While Looking at the closest pair, A\* search had to search a total of $8113$ nodes to find a solution. This was expectedly the worst performance since the closest distance is dominated by the other heuristics.
2. While looking at the farthest pair, A\* search did way better, only considering $119$ nodes before chancing upon a solution.
3. However, the containing box's Manhattan distance gave the best performance of all, with A\* search only searching $107$ nodes to find a solution.

#### Implementation Discusison

##### Priority Queue Implementation

To use *A\* search*, I implemented a [Priority Queue](priorityqueue.py) supporting the following methods:

```python
    def push(self, item):
        """Push an item with a priority to the queue.
        """
        heappush(self._heap, item)

    def pop(self):
        """Pop the item with the highest priority from the queue.
        """
        if not self._heap:
            raise IndexError('Pop from empty queue.')
        
        return heappop(self._heap)
    
    def is_empty(self):
        """Check if the queue is empty.
        """
        if not self._heap:
            return True
        return False
```

The methods are used in the *A\* search algorithm* to order search nodes by heuristics.

##### A\* Search's Search Nodes and Back-chaining

I used a custom class, *AStarNode*, to store node information while searching the Graph. The node system is a linked tree where each node has a pointer to its parent. Once the goal state is found, we backtrack to find the path taken....

```python
class AstarNode:
    # each search node except the root has a parent node
    # and all search nodes wrap a state object

    def __init__(self, state, heuristic, parent=None, transition_cost=0):
        self.state = state
        self.heuristic = heuristic
        self.parent = parent
        self.transition_cost = transition_cost
        

    def priority(self):
        """Return the current Node's priority value.
            This value is the sum of the transition cost
            to the Node and the heuristic estimating distance
            to the goal state.
        """
        return self.heuristic + self.transition_cost

    # Comparators for the heapq module.
    # These functions are used ot devise an ordering for AstarNode instances,
    # in order to arrange them in the priority queue.
    def __gt__(self, other):
        return self.priority() > other.priority()
    
    def __lt__(self, other):
        return self.priority() < other.priority()
    
    def __eq__(self, other):
        return self.priority() == other.priority()
    
    def __ge__(self, other):
        return self.priority() >= other.priority()
    
    def __le__(self, other):
        return self.priority() <= other.priority()
    

def backchain(node):
    """
        Backtrack and rebuild the path generated by the search.
    """
    
    # initialize an array to hold the sequence of states in the path.
    result = []
    current = node
    
    # backtrack until the root node is reached, 
    # i.e. a node is found whose predecessor is None.
    while current:
        
        # append states to the path.
        result.append(current.state)
        current = current.parent

    # reverse the path to get the correct order, and return the result.
    result.reverse()
    return result
```

##### A\* Search Implementation

I implemented A\* using the above Priority Queue, which offers a nicer interface than direct use of `heapq`'s `heappush` and `heappop` functions.

```python
INFINITY = 2**20

def astar_search(search_problem, heuristic_fn):
    """Run A* search on the search problem with the specified heuristic function."""
    
    # initialize the handler for the search solution.
    solution = SearchSolution(search_problem, "Astar with heuristic " + heuristic_fn.__name__)
    
    # initialize the start node and priority queue,
    # then push the start node into the queue.
    start_node = AstarNode(search_problem.start_state, heuristic_fn(search_problem.start_state))
    queue = PriorityQueue()
    queue.push(start_node)

    # initilize a dictionary to hold states and associated costs
    # to avoid evaluating paths that have been superseded by lesser-cost paths.
    visited_cost = {}
    visited_cost[start_node.state] = 0

    # while priority queue is not empty (i.e. there are still nodes to explore)...
    while queue:
        
        # get node in front of priority queue and check it's state.
        current_node = queue.pop()
        current_state = current_node.state
        
        # if the node has been superseded by another node (for the same state) 
        # that had a lesser cost, skip the current node
        # and proceed to the next node in the queue.
        if visited_cost[current_state] != current_node.transition_cost:
            continue
            
        solution.nodes_visited = solution.nodes_visited + 1
        
        # if current state the goal state, backtrack and rebuild the path.
        if search_problem.is_goal(current_state):
            solution.cost = visited_cost[current_state]
            solution.path = backchain(current_node)
            break
        
        # if current node is not the goal state:
        #   1. get cost of current state and compute cost for next state.
        current_cost = current_node.transition_cost
        next_cost = current_cost + 1
        
        #   2. get all possible next states for the current state
        #   3. for each next state, calculate the cost of the transition 
        #      using the cost to current, transition cost, and heuristic and cost to current.
        for next_state in search_problem.get_successors(current_state):
        
            #   4. if a node's new cost is more favorable than its current cost,
            #      save the new cost to the costs dictionary and push it into the priority queue.
            if visited_cost.get(next_state, INFINITY) > next_cost:
                visited_cost[next_state] = next_cost
                next_node = AstarNode(next_state, heuristic_fn(next_state),
                                      parent=current_node, transition_cost=next_cost)
                queue.push(next_node)
                

    # once the priority queue is empty or an exit occurs 
    # (i.e. a goal state has been found), return the solution.
    return solution
```

##### Getting Successors; Mazeworld

In the Mazeworld, only a single robot can move at a time, collissions are not allowed, and the goal state is the state that exactly matches whatever state was specified at the beginnign of the search.

```python
def get_successors(self, state):
        """
        Returns a list of (action, state, cost) tuples corresponding to edges in the graph.
        """
        
        # Initialzie successors, 
        # loop over all bots and find their possible next movements,
        # and add them to the array of possible next states.
        
        successors = []
        num_bots = len(state) // 2
        
        for bot in range(num_bots):
            ix = 2 * bot
            iy = ix + 1
            x, y = state[ix], state[iy]
            
            for step in [-1, 1]:
                # if bot can move in x direction, add to successors.
                if self.maze.can_move(x+step, y, state):
                    
                    new_state = self.move(state, index=ix, new_val=x+step)
                    successors.append(new_state)
                    
                # if bot can move in y direction, add to successors.
                if self.maze.can_move(x, y+step, state):
                    
                    new_state = self.move(state, index=iy, new_val=y+step)
                    successors.append(new_state)

        # return compiled array of successors
        return successors
    

def move(self, state, index=None, new_val=None):
    """
        Given a state and an action, returns the new state.
    """
    
    # initialize next state 
    next_state = []
    
    # copy values from original state, swapping out the value at index with new_val
    for i in range(len(state)):
        if i == index:
            next_state.append(new_val)
        else:
            next_state.append(state[i])
            
    # return an immutable tuple of the new state.
    return tuple(next_state)
                

def is_goal(self, state):
    """
        Check if a given state is the goal state for a game instance.
    """
    
    # loop over the state, checking if all positions match the goal state.
    for i in range(len(state)):
        if state[i] != self.goal_locations[i]:
            return False
    return True
```

##### Getting Successors; Blind Robot

In the Blind Robot problem, collissions are allowed and the goal location is the one where each robot in the Maze is standing in the same location. Furthermore, each robot must take every step made; whether it actually moves or not depends on the Maze.

```python
def get_successors(self, state):
        """
        Returns a list of (action, state, cost) tuples corresponding to edges in the graph.
        """
        
        # Initialzie successors, 
        # for each possible robot location, attempt to move it
        # in the appropriate direction.
        successors = []
        
        for step in [-1, 1]:
            
            next_state_x = self.move(state, step, dir_x=True)
            next_state_y = self.move(state, step, dir_y=True)
            
            if next_state_x:
                successors.append(next_state_x)
                
            if next_state_y:
                successors.append(next_state_y)


        # return compiled array of successors
        return successors

    
def move(self, state, step, dir_x=False, dir_y=False):
    """
        Given a state and an action, returns the new state.
    """
    
    # initialize next state
    # For each possible direction of movement,
    # attempt to move every robot in that direction.
    # If resulting state is distinct from the current state (i.e. someone moved),
    # return it as a valid state.
    # NOTE: collisions are allowed -- 
    # since the ultimate goal is to converge all the robots into a single point, anyway.
    
    if not dir_x and not dir_y:
        print("Error: Please specify a direction to move in. Set either `dir_x` or `dir_y` to `True`.")
        return None
    
    next_state = []
    for i in range(0, len(state), 2):
        
        ix, iy = i, i+1
        if dir_x and self.maze.is_floor(state[ix]+step, state[iy]):
            next_state.append(state[ix]+step)
            next_state.append(state[iy])
            continue
            
        elif dir_y and self.maze.is_floor(state[ix], state[iy]+step):
            next_state.append(state[ix])
            next_state.append(state[iy]+step)
            continue
        
        next_state.append(state[ix])
        next_state.append(state[iy])


    # if no one moved, discard the state.
    if state == next_state:
        return None
        
    #return immutable copy of the state.
    return tuple(next_state)



def _state(self, state):
    """
        This method, given a final state, collapses the locations into a tuple of unique items.
        This method is used internally and should not be used from outside the module.
        :arg state: The state to be converged.
    """
    
    _state = set()
    for i in range(0, len(state), 2):
        _state.add( (state[i], state[i+1]) )
        
    return tuple(_state) 


def is_goal(self, state):
    """
        Given a state, returns True if it is a goal state,
        i.e. all the robot start locations have converged.
    """
    _state = self._state(state)
    return len(_state) == 1
```

### Demonstration of Results

#### Mazeworld

##### Start State

```text
Maze:
###############
#C...........D#
#.............#
#.............#
#.............#
#.............#
#.............#
#.............#
#.............#
#.............#
#.............#
#.............#
#.............#
#A...........B#
###############
```

##### Halfway through

```text
Maze:
###############
#.............#
#.............#
#.............#
#.............#
#.............#
#.......B.....#
#........A....#
#.............#
#.............#
#..........C..#
#.............#
#.............#
#D............#
###############
```

##### Final State

```text
###############
#B...........A#
#.............#
#.............#
#.............#
#.............#
#.............#
#.............#
#.............#
#.............#
#.............#
#.............#
#.............#
#D...........C#
###############
```

##### Summary of Results

```text
----
Mazeworld problem:
Goal state:(13, 13, 1, 13, 13, 1, 1, 1)
Maze:
###############
#C...........D#
#.............#
#.............#
#.............#
#.............#
#.............#
#.............#
#.............#
#.............#
#.............#
#.............#
#.............#
#A...........B#
###############


attempted with search method Astar with heuristic manhattan_heuristic
number of nodes visited: 9246
solution length: 97
cost: 96
path: ...
```

#### Blind Robot

##### Start State

```text
Maze:
###############
#C...........D#
#.............#
#.............#
#.............#
#.............#
#.............#
#.............#
#.............#
#.............#
#.............#
#.............#
#.............#
#A...........B#
###############
```

##### Halfway Through

```text
Maze:
###############
#.............#
#C...D........#
#.............#
#.............#
#.............#
#.............#
#.............#
#.............#
#.............#
#.............#
#.............#
#.............#
#A...B........#
###############
```

##### Final State

```text
###############
#.............#
#.............#
#.............#
#.............#
#.............#
#.............#
#.............#
#.............#
#.............#
#.............#
#.............#
#.............#
#D............#
###############
```

##### Results Summary

```text
----
Blind robot problem: Possible start locations: (1, 1, 13, 1, 1, 13, 13, 13)
Maze:
###############
#C...........D#
#.............#
#.............#
#.............#
#.............#
#.............#
#.............#
#.............#
#.............#
#.............#
#.............#
#.............#
#A...........B#
###############


attempted with search method Astar with heuristic manhattan_heuristic
number of nodes visited: 107
solution length: 25
cost: 24
path: ...

Directions to take:
['W', 'W', 'W', 'W', 'W', 'S', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S']
Final position = (1, 1)
```

### Extra Implementations

Here is a version of the 8-Puzzle problem.

###### Start state

```python
Maze:
#####
#FBA#
#EDG#
#.HC#
#####
```

###### Goal state

```text
#####
#FGH#
#CDE#
#.AB#
#####
```

###### Search results

```text
----
Mazeworld problem:
Goal state:(2, 1, 3, 1, 1, 2, 2, 2, 3, 2, 1, 3, 2, 3, 3, 3)
Maze:
#####
#FBA#
#EDG#
#.HC#
#####


attempted with search method Astar with heuristic manhattan_heuristic
number of nodes visited: 958
solution length: 25
cost: 24
path: ...
```
