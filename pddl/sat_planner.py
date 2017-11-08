#!/usr/bin/env python
# Four spaces as indentation [no tabs]

from pddl.PDDL import PDDL_Planner
from structures.domain import Domain

from itertools import combinations

class SAT_Planner(PDDL_Planner):

    def solve(self, domain, initial_state, goal_state):
        # encode the problem
        limit = 4
        for length in range(0,limit):
            formula = self.encode_formula(domain, initial_state, goal_state, length)
            print formula
        return None

    def encode_formula(self, actions, initial_state, goal_state, plan_length):
        # Parsed data
        domain = Domain(actions)
        preds = domain.all_facts
        state = initial_state
        goal_pos = goal_state[0]
        goal_not = goal_state[1]

        # Encode initial state
        s0_formula = ""
        for pred in initial_state:
            s0_formula+= self.prop_at(pred,0)+" "
        s0_formula = self.land(s0_formula)

        # Encode goal state
        goal_formula = ""
        for pred in goal_pos:
            goal_formula+= self.prop_at(pred, plan_length) + " "

        for pred in goal_not:
            goal_formula+= self.lnot(self.prop_at(pred, plan_length)) + " "

        goal_formula = self.land(goal_formula)

        pred_declaration = ""
        action_formula = ""
        exclusion_axiom = ""

        for i in range(0,plan_length+1):
            for p in preds:
                pred_declaration += self.z3_const(self.prop_at(p, i))

        #encode stuff over the length of the plan
        for i in range(0,plan_length):
            action_names = []
            #Encode actions
            for action in actions:
                action_names.append(self.action_prop_at(action,i))
                action_formula+=self.action(action,i)+ " "

            #Encode exclusion axioms
            for (a1,a2) in combinations(action_names,2):
                exclusion_axiom += self.lnot(self.lor("{0} {1}".format(a1,a2) ))


            #Encode frame axioms
            #TODO Still need to encode frame axioms


            # Build Z3 formulas
            for a in action_names:
                pred_declaration += self.z3_const(a)

        st = pred_declaration+"\n"
        st += self.z3_assert(s0_formula) + "\n"
        st += self.z3_assert(goal_formula) + "\n"
        st += self.z3_assert(self.land(action_formula))+"\n"
        st += self.z3_assert(self.land(exclusion_axiom))+"\n"
        return st

    def action(self,action,t):
        st = ""
        ant = self.action_prop_at(action,t)#TODO Add parameters when we start to deal with FOL
        precond = ""
        for pred in action.positive_preconditions:
            precond += self.prop_at(pred,t)+" "
        for pred in action.negative_preconditions:
            precond += self.lnot(self.prop_at(pred,t))+" "

        effect = ""
        for pred in action.add_effects:
            effect += self.prop_at(pred, t+1) + " "
        for pred in action.del_effects:
            effect += self.lnot(self.prop_at(pred, t+1)) + " "

        cons = self.land(self.land(precond)+" "+self.land(effect))

        st = self.limply(ant, cons)
        return st

    def z3_assert(self,formula):
        return "(assert {0})".format(formula)

    def z3_const(self, pred):
        return "(declare-const {0} Bool)\n".format(pred)

    def lnot(self, formula):
        return "(not {0})".format(formula)

    def limply(self, antecedent, consequent):
        return "(implies {0} {1})".format(antecedent,consequent)

    def lor(self,formula):
        return "(or {0})".format(formula)

    def land(self,formula):
        return "(and {0})".format(formula)

    def action_prop_at(self,action,t):
        return self.prop_at((action.name,),t)

    def prop_at(self, prop, t):
        st = ""
        for term in prop:
            st+= str(term)+"_"
        return st+str(t)