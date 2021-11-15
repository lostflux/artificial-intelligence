#!/usr/bin/env python3

s = """
The preceding section developed algorithms for temporal probabilistic reasoning
using a general framework that was independent of the specific form of the 
transition and sensor models. In this and the next two sections, 
we discuss more concrete models and applications that illustrate 
the power of the basic algorithms and in some cases allow further 
improvements. We begin with the hidden Markov model,or HMM. 
An HMM is a temporal probabilistic model in which the state 
of the process is described by a single discrete random variable. 
The possible values of the variable are the possible states of the 
world. The umbrella example described in the preceding section is 
therefore an HMM, since it has just one state variable: Raint. 
"""

s = s.strip().replace.replace(' ', '')


with open("mazes/maze6.maz", "w") as f:
    f.write(s)