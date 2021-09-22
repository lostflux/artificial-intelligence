class FoxProblem:
    def __init__(self, start_state=(3, 3, 1)):
        self.start_state = start_state
        self.goal_state = (0, 0, 0)
        self.state = start_state
        self.chickens = start_state[0]
        self.foxes = start_state[1]
        self.boat_ashore = bool(start_state[2])

        # you might want to add other things to the problem,
        #  like the total number of chickens (which you can figure out
        #  based on start_state

    # get successor states for the given state
    def get_successors(self, state):
        # you write this part. I also had a helper function
        #  that tested if states were safe before adding to successor list
        next_states = set()
        for num_chickens in range(0, 3):
            for num_foxes in range(0, 3):
                if 0 < (num_chickens + num_foxes) <= 2:                  # ignore states the empty transition
                    new_chickens = self.chickens - num_chickens         # find new number of chicken ashore
                    new_foxes = self.foxes - num_foxes                  # find new number of foxes ashore
                    boat_status = not self.boat_ashore                  # flip boat status
                    state = (new_chickens, new_foxes, int(boat_status))

                    # check the state for validity, append to valid states
                    if self.is_valid(state):
                        next_states.add(state)

        # return set of states
        return next_states

    # I also had a goal test method. You should write one.
    def goal_state(self, state):
        return self.goal_state == state

    @staticmethod
    def is_valid(state):
        return state[0] >= state[1]

    def __str__(self):
        string =  "Chickens and foxes problem: " + str(self.start_state)
        return string


## A bit of test code

if __name__ == "__main__":
    test_cp = FoxProblem((5, 5, 1))
    print(test_cp.get_successors((5, 5, 1)))
    print(test_cp)
