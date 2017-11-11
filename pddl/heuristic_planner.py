from pddl.PDDL import PDDL_Planner
import Queue
import sys

class Heuristic(object):

    def h(self,domain,s0,goal):
        raise NotImplementedError("Unimplemented")


class MaxHeuristic(Heuristic):

    def h(self,actions,initial_state,goal_state):
        last_state = set([])
        reachable_literals = set(initial_state)
        positive_goals = set(goal_state[0])

        positive_effects = set([])
        negative_effects = set([])
        for a in actions:
            positive_effects = positive_effects.union(set(a.add_effects))
            negative_effects = negative_effects.union(set(a.del_effects))
        # First check the obvious stuff
        for p in goal_state[0]:
            if p not in reachable_literals and p not in positive_effects:
                return False
        for p in goal_state[1]:
            if p in reachable_literals and p not in negative_effects:
                return False

        max = 0
        while last_state != reachable_literals:
            max+=1
            last_state = reachable_literals.copy()
            if positive_goals.issubset(reachable_literals):
                return max
            for a in actions:
                if a.applicable(reachable_literals):
                    reachable_literals = reachable_literals.union(a.add_effects)

        return sys.maxint

class Heuristic_Planner(PDDL_Planner):

    def __init__(self,heuristic=MaxHeuristic()):
        self.h = heuristic

    # -----------------------------------------------
    # Solve
    # -----------------------------------------------

    def solve(self, domain, initial_state, goal_state):

        # Parsed data
        actions = domain
        state = frozenset(initial_state)
        goal_pos = frozenset(goal_state[0])
        goal_not = frozenset(goal_state[1])
        cost = {}
        cost[state] = 0
        # Do nothing
        if self.applicable(state, goal_pos, goal_not):
            return []
        # Search
        visited = set([state])
        # fringe = [state, None]
        fringe = Queue.PriorityQueue()
        fringe.put((state,None),0)
        while fringe:
            # state = fringe.pop(0)
            # plan = fringe.pop(0)
            g = cost[state]
            state, plan = fringe.get()
            g+=1
            cost[state] = g
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
                        f = g+self.h.h(actions,state,goal_state)
                        fringe.put((new_state, (act, plan)),f)
        return None

# ==========================================
# Main
# ==========================================
if __name__ == '__main__':
    import sys
    domain = sys.argv[1]
    problem = sys.argv[2]
    planner = Heuristic_Planner()
    plan = planner.solve_file(domain, problem)
    if plan:
        print('plan:')
        for act in plan:
            print(act)
    else:
        print('No plan was found')