
# COSC 76: Artificial Intelligence

## Programming Assignment 4: Constraint Satisfaction Problems

### Student: Amittai Wekesa (github: @siavava)

### Fall 2021

In this programming assignment, you will write a general-purpose constraint solving algorithm, and apply it to solve different CSPs. The learning objective is to implement the methods to solve the CSP, discussed in class. While there can be other previous classes that are useful, the main material covered with this assignment is from 10/4 to 10/8 included, i.e., the PDFs lec10 and lec11.

## **Getting started**

To give you the opportunity to build the code from scratch, this time there is no provided code. If you want, you can take a look at the "Design notes" below, based on our implementation, after the description of the "Required tasks". You are also welcome to come up with your design ideas.

The material in the AIMA book (Chapter 6.1-6.3) and at the class meetings will give you a reference too.

## **REQUIRED TASKS**

### 1. CSP problem - start with map coloring

Develop a framework that poses the map-coloring problem (as described in the book) as a CSP that the solver can solve.

As a reminder, the map-coloring problem involves several binary constraints. For each pair of adjacent countries, there is a binary constraint that prohibits those countries from having the same color.

#### CSP Implementation

To represent the problem, I built a [CSP abstraction](CSP.py) that tracks variables, domains, and constraints. It also tracks whether certain heuristics have been enabled or disabled, and if, for instance, debug mode is on or off. The absjtraction also provides a nice interface to outsiders to poll whether a given assignment satisfies the CSP constraints or is a complete assignment.

After some experimentation, I implemented the backtracking algorithm in a separate [file](backtracking.py). This makes it easier to have the main interface to the algorithm call separate recursive functions depending on whether inferencing is enabled or not.

**Since the code is really long (200+ lines), I did't include it in the report. Check out [CSP.py](CSP.py) and [backtracking.py](backtracking.py) to see the code.

#### Results

To see the results for this test case, run `test3()` in [test_csp.py](test_csp.py).

Occassionally, the algorithm finds a solution in 8 calls to `backtrack`, suggesting that it got every variable right on first assignment. However, this doesn't always happen and sometimes the algorithm takes as long as 50 calls! Clearly, there's a lot of inconsistency.

##### **Take 1; solution in 8**

```text
./test_csp.py

...
CSP
        variables:      {'WA', 'NT', 'NSW', 'SA', 'Q', 'T', 'V'}                     
        domains :       {'WA': {'R'}, 'NT': {'G', 'B', 'R'}, 'Q': {'G', 'B', 'R'}, 'NSW': {'G', 'B', 'R'}, 'V': {'G', 'B', 'R'}, 'SA': {'G', 'B', 'R'}, 'T': {'G', 'B', 'R'}}                     
        constraints :   {('SA', 'NSW'), ('WA', 'SA'), ('SA', 'V'), ('NSW', 'V'), ('NT', 'Q'), ('WA', 'NT'), ('SA', 'NT'), ('SA', 'Q'), ('Q', 'NSW')}                     
        solution:       {'WA': 'R', 'NT': 'G', 'NSW': 'G', 'SA': 'B', 'Q': 'R', 'T': 'G', 'V': 'R'}                     
...
  
         109 function calls (102 primitive calls) in 0.000 seconds

   Ordered by: cumulative time

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    0.000    0.000    0.000    0.000 ./test_csp.py:62(test3)
        1    0.000    0.000    0.000    0.000 /workspace/personal/python/cs76/PA4/erratum.py:37(log_info)
        1    0.000    0.000    0.000    0.000 /workspace/personal/python/cs76/PA4/backtracking.py:18(backtracking_search)
**->  8/1    0.000    0.000    0.000    0.000 /workspace/personal/python/cs76/PA4/backtracking.py:25(backtrack)
        1    0.000    0.000    0.000    0.000 {built-in method builtins.print}
       12    0.000    0.000    0.000    0.000 /workspace/personal/python/cs76/PA4/CSP.py:134(is_consistent)
        1    0.000    0.000    0.000    0.000 /workspace/personal/python/cs76/PA4/CSP.py:54(__str__)
       25    0.000    0.000    0.000    0.000 /workspace/personal/python/cs76/PA4/CSP.py:119(satisfies_constraint)
        1    0.000    0.000    0.000    0.000 /workspace/personal/python/cs76/PA4/CSP.py:21(__init__)
       34    0.000    0.000    0.000    0.000 {built-in method builtins.len}
        8    0.000    0.000    0.000    0.000 /workspace/personal/python/cs76/PA4/CSP.py:148(is_completed)
        7    0.000    0.000    0.000    0.000 /workspace/personal/python/cs76/PA4/CSP.py:104(get_unassigned_variable)
        1    0.000    0.000    0.000    0.000 /workspace/personal/python/cs76/PA4/erratum.py:18(__text_color)
        7    0.000    0.000    0.000    0.000 /workspace/personal/python/cs76/PA4/CSP.py:85(order_values)
        1    0.000    0.000    0.000    0.000 {method 'disable' of '_lsprof.Profiler' objects}
```

##### **Take 2; Solution in 50**

```text
./test_csp.py

...
CSP
        variables:      {'Q', 'NT', 'NSW', 'SA', 'T', 'V', 'WA'}                     
        domains :       {'WA': {'R'}, 'NT': {'B', 'G', 'R'}, 'Q': {'B', 'G', 'R'}, 'NSW': {'B', 'G', 'R'}, 'V': {'B', 'G', 'R'}, 'SA': {'B', 'G', 'R'}, 'T': {'B', 'G', 'R'}}                     
        constraints :   {('SA', 'NSW'), ('NT', 'Q'), ('WA', 'SA'), ('SA', 'NT'), ('WA', 'NT'), ('SA', 'Q'), ('NSW', 'V'), ('SA', 'V'), ('Q', 'NSW')}                     
        solution:       {'Q': 'R', 'NT': 'B', 'NSW': 'B', 'SA': 'G', 'T': 'B', 'V': 'R', 'WA': 'R'}                     
...
  
         827 function calls (778 primitive calls) in 0.001 seconds

   Ordered by: cumulative time

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    0.000    0.000    0.001    0.001 ./test_csp.py:62(test3)
        1    0.000    0.000    0.001    0.001 /workspace/personal/python/cs76/PA4/backtracking.py:18(backtracking_search)
**-> 50/1    0.000    0.000    0.001    0.001 /workspace/personal/python/cs76/PA4/backtracking.py:25(backtrack)
      114    0.000    0.000    0.000    0.000 /workspace/personal/python/cs76/PA4/CSP.py:134(is_consistent)
      228    0.000    0.000    0.000    0.000 /workspace/personal/python/cs76/PA4/CSP.py:119(satisfies_constraint)
        1    0.000    0.000    0.000    0.000 /workspace/personal/python/cs76/PA4/erratum.py:37(log_info)
        1    0.000    0.000    0.000    0.000 {built-in method builtins.print}
      279    0.000    0.000    0.000    0.000 {built-in method builtins.len}
       49    0.000    0.000    0.000    0.000 /workspace/personal/python/cs76/PA4/CSP.py:104(get_unassigned_variable)
       50    0.000    0.000    0.000    0.000 /workspace/personal/python/cs76/PA4/CSP.py:148(is_completed)
        1    0.000    0.000    0.000    0.000 /workspace/personal/python/cs76/PA4/CSP.py:54(__str__)
       49    0.000    0.000    0.000    0.000 /workspace/personal/python/cs76/PA4/CSP.py:85(order_values)
        1    0.000    0.000    0.000    0.000 /workspace/personal/python/cs76/PA4/CSP.py:21(__init__)
        1    0.000    0.000    0.000    0.000 /workspace/personal/python/cs76/PA4/erratum.py:18(__text_color)
        1    0.000    0.000    0.000    0.000 {method 'disable' of '_lsprof.Profiler' objects}
```

### 2. Heuristics

Add the heuristics we have seen in class (MRV, degree heuristic, LCV). Make it easy to enable or disable each, since you will want to compare the effectiveness of your results, and since that will aid debugging.

I implemented the Heuristics in a separate [heuristics](heuristics.py). Since they're implemented as external functions (as opposed to actual code within methods in the CSP class), it's easier to simply call the functions and inspect / debug code specific to the heuristics.

```python

```

### 3. Inference

Add an inference technique (AC-3). Make it easy to enable or disable inference, since you will need to test effectiveness.

I implemented inferencing (AC-3) in [inferences.py](inferences.py). The inference functionality modifies the CSP domains, which (after a lot of debugging) inspired me to separate the backtracking algorithm with inferencing from the baseline algorithm.

### 4. Test on map coloring

You can test your solver with and without heuristics and inference on the map-coloring problem, and describe it in the writeup.

### 5. New problem: Circuit-board layout problem

Write code that describes and solves the circuit-board layout problem. Solve it for at least the example case I have suggested. You should not have to write any more backtracking code; you should be able to use the same implementation you used for map-coloring.

Details about the problem
You are given a rectangular circuit board of size n x m, and k rectangular components of arbitrary sizes.  Your job is to lay the components out in such a way that they do not overlap.  For example, maybe you are given these components:

```text
      bbbbb   cc
aaa   bbbbb   cc  eeeeeee
aaa           cc
```

and are asked to lay them out on a 10x3 grid

```text
..........
..........
..........
```

A solution might be

```text
eeeeeee.cc
aaabbbbbcc
aaabbbbbcc
```

Notice that in this case the solution is not unique!

The variables for this CSP will be the locations of the lower left corner of each component.  Assume that the lower left corner of the board has coordinates (0, 0).  

Make sure your code displays the output in some nice (enough) way.  ASCII art would be fine.

A particularly strong solution might consider several boards, of different sizes and with different numbers, sizes, and shapes of parts.

Discussion points for the write-up
In your write-up, describe the domain of a variable corresponding to a component of width w and height h, on a circuit board of width n and height m.  Make sure the component fits completely on the board.

Consider components a and b above, on a 10x3 board.  In your write-up, write the constraint that enforces the fact that the two components may not overlap.  Write out legal pairs of locations explicitly.

Describe how your code converts constraints, etc, to integer values for use by the generic CSP solver.
