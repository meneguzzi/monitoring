from structures.state import State
from copy import deepcopy

class Action:
    # TODO possibly move this to another class
    # TODO accept propositional PDDL

    def __init__(self,name,pre,addList,delList=[]):
        self.name = name
        self.pre = pre
        self.addList = addList
        self.delList = delList

    def allFacts(self):
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
            # print State(self.addList)
            s2 = s2 + State(self.addList)
            return s2
        else:
            raise ValueError(str(self)+' is not applicable to '+str(state))

    def __repr__(self):
        return "<"+self.name+","+str(self.pre)+","+str(self.delList)+","+str(self.addList)+">"