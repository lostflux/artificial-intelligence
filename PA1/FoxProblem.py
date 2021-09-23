class FoxProblem:
    def __init__(self, start_state=(3, 3, 1)):
        self.start_state = start_state
        self.goal_state = (0, 0, 0)
        self.state = start_state
        self.max_chickens = start_state[0]
        self.max_foxes = start_state[1]
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
                if 0 < (num_chickens + num_foxes) <= 2:  # ignore states the empty transition
                    if bool(state[2]):

                        # BOAT LEAVING SHORE
                        new_chickens = state[0] - num_chickens  # find new number of chicken ashore
                        new_foxes = state[1] - num_foxes  # find new number of foxes ashore
                        boat_ashore = not bool(state[2])  # flip boat status
                        next_state = (new_chickens, new_foxes, int(boat_ashore))

                        # check the state for validity, append to valid states
                        if self.is_valid(next_state):
                            next_states.add(next_state)
                    else:

                        # BOAT RETURNING TO SHORE
                        new_chickens = state[0] + num_chickens  # find new number of chicken ashore
                        new_foxes = state[1] + num_foxes  # find new number of foxes ashore
                        boat_ashore = not bool(state[2])  # flip boat status
                        next_state = (new_chickens, new_foxes, int(boat_ashore))

                        # check the state for validity, append to valid states
                        if self.is_valid(next_state):
                            next_states.add(next_state)
        # return set of states
        return next_states

    # I also had a goal test method. You should write one.
    def is_goal(self, state):
        return self.goal_state == state

    def is_valid(self, state):

        if state[0] <= self.max_chickens and state[1] <= self.max_foxes:
            return 0 <= state[1] <= state[0]

        return False

    def __str__(self):
        string = "Chickens and foxes problem: " + str(self.start_state)
        return string


## A bit of test code

def check_states(state, goal_state):
    if state == goal_state:
        print("Found!")
        return

    print(test_cp.get_successors(state))
    for n_state in test_cp.get_successors(state):
        check_states(n_state, goal_state)


if __name__ == "__main__":
    test_cp = FoxProblem((5, 5, 1))
    print(test_cp.get_successors((5, 5, 1)))
    start_state = (5, 5, 1)
    goal_state = (0, 0, 0)
    check_states(start_state, goal_state)
    # while True:

    print(test_cp)
