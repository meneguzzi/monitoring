from copy import deepcopy
from structures.sensor import Sensor
from itertools import chain, combinations


def powerset(iterable):
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))


class Domain():

    def __init__(self,actions):
        self.actions = {}
        for action in actions:
            self.actions[action.name] = action

    @property
    def all_facts(self):
        all_facts = set([fact for op in self.actions for fact in op.all_facts()])
        return all_facts

    def generate_state_space(self):
        all_facts = self.all_facts()
        return powerset(all_facts)

    def __getitem__(self, item):
        return self.actions[item]

    def __setitem__(self, key, value):
        self.actions[key] = value


class Action:
    # TODO accept propositional PDDL

    def __init__(self,name,pre,addList,delList=[]):
        self.name = name
        self.pre = pre
        self.addList = addList
        self.delList = delList

    def all_facts(self):
        facts = []
        facts += self.pre
        facts += self.addList
        facts += self.delList
        return set(facts)

    def applicable(self,state):
        return state.models(State(self.pre))

    def result(self,state):
        if(self.applicable(state)):
            s2 = deepcopy(state)
            s2 = s2 - State(self.delList)
            s2 = s2 + State(self.addList)
            return s2
        else:
            raise ValueError(str(self)+' is not applicable to '+str(state))

    def __repr__(self):
        return "<"+self.name+","+str(self.pre)+","+str(self.delList)+","+str(self.addList)+">"


class Trace():
    """ A trace from a plan, this should consist of a sequence of states"""

    def __init__(self, trace):
        self.trace = trace

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

class State():

    def __init__(self,facts=None):
        ## A state has a dictionary of facts
        self.facts = set([])
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

    def __str__(self):
        return str("State: "+str(list(self.facts)))

    def __repr__(self):
        return str(list(self.facts))


if __name__ == '__main__':
    s = State(['p','q'])

    s1 = State(['p','q'])
    s2 = State(['p','q'])
    s3 = State(['q'])

