from copy import deepcopy
from structures.sensor import Sensor
from itertools import chain, combinations


def powerset(iterable):
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))


class Problem():
    def __init__(self, initial_state, goal_state):
        self.initial_state = initial_state
        self.goal_state = goal_state


class Domain():

    def __init__(self,actions):
        self.ss = None
        self.actions = {}
        for action in actions:
            self.actions[action.name] = action

    @property
    def all_facts(self):
        all_facts = set([fact for op in self.actions.values() for fact in op.all_facts()])
        return all_facts

    @property
    def state_space(self):
        if self.ss is None:
            self.ss = [s for s in self.generate_state_space()]
        return self.ss

    def generate_state_space(self):
        return powerset(self.all_facts)

    def groundify(self):
        return Domain([action.groundify() for action in self.actions.values()])

    def __iter__(self):
        return iter(self.actions.values())

    def __getitem__(self, item):
        return self.actions[item]

    def __setitem__(self, key, value):
        self.actions[key] = value


class Action:
    # TODO accept propositional PDDL

    def __init__(self, name, parameters, positive_preconditions, negative_preconditions, add_effects, del_effects=[], cost = 0):
        self.name = name
        self.parameters = parameters
        self.positive_preconditions = positive_preconditions
        self.negative_preconditions = negative_preconditions
        self.add_effects = add_effects
        self.del_effects = del_effects if del_effects is not None else []
        self.cost=0

    def all_facts(self):
        facts = []
        # TODO we need to change this to separate ground from lifted operators, now I'm assuming it's propositional
        # facts += [str(prop) for prop in self.positive_preconditions]
        # facts += [str(prop) for prop in self.negative_preconditions]
        # facts += [str(prop) for prop in self.add_effects]
        # facts += [str(prop) for prop in self.del_effects]
        facts += self.positive_preconditions
        facts += self.negative_preconditions
        facts += self.add_effects
        facts += self.del_effects
        return set(facts)

    def applicable(self,state):
        # return state.models(State(self.positive_preconditions))
        for i in self.positive_preconditions:
            if i not in state:
                return False

        for i in self.negative_preconditions:
            if i in state:
                return False

        return True

    def result(self,state):
        if self.applicable(state):
            s2 = deepcopy(state)
            s2 = s2 - State(self.del_effects)
            s2 = s2 + State(self.add_effects)
            return s2
        else:
            raise ValueError(str(self)+' is not applicable to '+str(state))

    def groundify(self):
        return Action(self.name,tuple(self.parameters),
                      [tuple(fact) for fact in self.positive_preconditions],
                      [tuple(fact) for fact in self.negative_preconditions],
                      [tuple(fact) for fact in self.add_effects],
                      [tuple(fact) for fact in self.del_effects] if self.del_effects is not None else None,
                      self.cost)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __hash__(self):
        #return hash((self.positive_preconditions,self.negative_preconditions,self.add_effects,self.del_effects))
        return hash((self.name,self.parameters)) # This should work even in the ground case.

    def __repr__(self):
        return "<"+self.name+","+str(self.parameters)+","+str(self.positive_preconditions)+","+str(self.negative_preconditions) + \
               "," + str(self.add_effects) + "," + str(self.del_effects) + ","+str(self.cost) +  ">"


class Trace():
    """ A trace from a plan, this should consist of a sequence of states"""

    def __init__(self, trace):
        self.trace = tuple(trace)

    def __setitem__(self, key, value):
        if isinstance(value, State):
            self.trace[key] = value
        else:
            raise ValueError('Value is not a state.')

    def __getitem__(self, item):
        return self.trace[item]

    def models(self, sensor, state, domain):
        assert isinstance(sensor, Sensor)
        assert isinstance(state, State)
        return sensor.is_model_of(self, state, domain)

    def __repr__(self):
        return repr(self.trace)

    def __len__(self):
        return len(self.trace)

    def __hash__(self):
        # TODO Reimplement this horribly inefficient mechanism
        return hash(self.trace)

    def __eq__(self, other):
        if isinstance(other, Trace) and len(self) == len(other):
            for i in range(len(other)):
                if(other[i] != self[i]):
                    return False
        else:
            return False

        return True

    @staticmethod
    def plan_to_trace(s0, plan):
        trace = [s0]
        for op in plan:
            assert(isinstance(op,Action))
            if op.applicable(trace[-1]):
                trace+=op.result(trace[-1])
            else:
                raise "Plan "+str(plan)+" contains invalid action "+str(op)
        return Trace(trace)


class State():

    def __init__(self,facts=None):
        ## A state has a dictionary of facts
        self.facts = frozenset([])
        if facts is not None:
            self.facts |= set(facts)

    def models(self, other):
        if isinstance(other,State):
            return other.facts.issubset(self.facts)
        elif isinstance(other,set):
            return other.issubset(self.facts)
        else:
            return other in self.facts

    def __contains__(self, item):
        return item in self.facts

    def __eq__(self, other):
        if isinstance(other,State):
            return self.facts == other.facts
        else:
            return False

    def __add__(self, other):
        if isinstance(other,State):
            self.facts |= other.facts
        else:
            self.facts |= set([other])
        return self

    def __setitem__(self, key, value):
        if key in self.facts and value is False:
            self.facts.remove(key)
        elif key not in self.facts and value:
            self.facts.add(key)
        else: # all other cases require nothing to be done
            pass

    def __getitem__(self, item):
        return item in self.facts

    def __sub__(self, other):
        if isinstance(other,State):
            self.facts -= other.facts
        else:
            self.facts.remove(other)
        return self

    def __hash__(self):
        return hash(self.facts)

    def __str__(self):
        return str("State: "+str(list(self.facts)))

    def __repr__(self):
        return str(list(self.facts))

    def __contains__(self, item):
        return item in self.facts

    def to_PDDL(self):
        str = "(and "
        for literal in self.facts:
            str += literal_to_pddl(literal)
        str += ")"
        return str


def literal_to_pddl(s):
    pddl = "("
    if s is list or s is tuple:
        for e in s:
            pddl+=" "+str(e)
    else:
        pddl +=str(s)
    pddl +=")"
    return pddl

if __name__ == '__main__':
    s = State(['p','q'])

    s1 = State(['p','q'])
    s2 = State(['p','q'])
    s3 = State(['q'])

