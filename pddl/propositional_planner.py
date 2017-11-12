#!/usr/bin/env python
# Four spaces as indentation [no tabs]

from pddl.PDDL import PDDL_Parser
from pddl.PDDL import PDDL_Planner
from structures.domain import State
import time

class Propositional_Planner(PDDL_Planner):

    def __init__(self, max_length=0, time_limit = 0):
        self.max_length = max_length
        self.time_limit = time_limit


    def tree_length(self,plan):
        length = 0
        while plan:
            length += 1
            act, plan = plan
        return length

    #-----------------------------------------------
    # Solve
    #-----------------------------------------------

    def solve(self, domain,initial_state,goal_state):

        if self.time_limit: start = time.time()
        # Parsed data
        actions = domain
        state = frozenset(initial_state)
        goal_pos = frozenset(goal_state[0])
        goal_not = frozenset(goal_state[1])
        # Do nothing
        if self.applicable(state, goal_pos, goal_not):
            return []
        # Search
        visited = set([state])
        fringe = [(state, None)]
        while fringe:
            # state = fringe.pop(0)
            # plan = fringe.pop(0)
            state, plan = fringe.pop(0)
            if self.max_length and plan is not None and self.tree_length(plan) > self.max_length: return None
            if self.time_limit and time.time() - start > self.time_limit: return None
            for act in actions:
                if self.applicable(state, act.positive_preconditions, act.negative_preconditions):
                    new_state = self.apply(state, act.add_effects, act.del_effects)
                    if new_state not in visited:
                        if self.applicable(new_state, goal_pos, goal_not):
                            full_plan = [act]
                            while plan:
                                act, plan = plan
                                full_plan.insert(0, act)
                            return full_plan
                        # visited.append(new_state)
                        visited.add(new_state)
                        fringe.append((new_state, (act, plan)))
        return None


def main(domain, problem):
    planner = Propositional_Planner()
    plan = planner.solve_file(domain, problem)
    if plan:
        print('plan:')
        for act in plan:
            print(act)
    else:
        print('No plan was found')


# ==========================================
# Main
# ==========================================
if __name__ == '__main__':
    import sys
    domain = sys.argv[1]
    problem = sys.argv[2]
    main(domain,problem)