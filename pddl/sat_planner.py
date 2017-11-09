#!/usr/bin/env python
# Four spaces as indentation [no tabs]

from pddl.PDDL import PDDL_Planner
from structures.domain import Domain

from itertools import combinations

from z3 import *

class SAT_Planner(PDDL_Planner):

    def __init__(self):
        self.props = dict()
        self.action_map = dict()
        self.max_length = 20


    def solve(self, domain, initial_state, goal_state):
        # encode the problem
        for length in range(0,self.max_length):
            s = Solver()
            self.props.clear()
            self.action_map.clear()
            self.encode_formula(s, domain, initial_state, goal_state, length)
            # print s.to_smt2()
            # print s
            if s.check() == sat:
                print "Model found with length {0}".format(length)
                # print s.model()
                plan = self.extract_plan(s.model(),length)
                # print plan
                return plan
            else:
                print "No model found with length {0}".format(length)
        return None


    def extract_plan(self, model, length):
        plan = [None for i in range(length)]
        for prop in model:
            if prop.name() in self.action_map.keys() and model[prop]:
                # print "Adding "+prop.name()
                (action,index) = self.action_map[prop.name()]
                plan[index] = action
        return plan



    def encode_formula(self, s, actions, initial_state, goal_state, plan_length):
        # Parsed data
        domain = Domain(actions)
        preds = domain.all_facts
        state = initial_state
        goal_pos = goal_state[0]
        goal_not = goal_state[1]

        # Encode initial state
        s0_formula = []
        # for pred in initial_state:
        #     s0_formula.append(self.prop_at(pred,0))
        for pred in preds:
            if pred in initial_state:
                s0_formula.append(self.prop_at(pred,0))
            else:
                s0_formula.append(Not(self.prop_at(pred, 0)))
        s0_formula = And(*s0_formula)

        # Encode goal state
        goal_formula = []
        for pred in goal_pos:
            goal_formula.append(self.prop_at(pred, plan_length))

        for pred in goal_not:
            goal_formula.append(Not(self.prop_at(pred, plan_length)))

        goal_formula = And(*goal_formula)

        action_formula = []
        exclusion_axiom = []
        frame_axioms = []

        for i in range(0,plan_length+1):
            for p in preds:
                self.prop_at(p, i)

        for i in range(0,plan_length):
            for a in actions:
                self.action_prop_at(a,i)

        #encode stuff over the length of the plan
        for i in range(0,plan_length):
            action_names = []
            #Encode actions
            for action in actions:
                action_names.append(self.action_prop_at(action,i))
                action_formula.append(self.action(action,i))

            #Encode exclusion axioms
            for (a1,a2) in combinations(action_names,2):
                exclusion_axiom.append(Or(Not(a1),Not(a2)))


            #Encode frame axioms (explanatory frame actions)
            for p in preds:
                add_eff_actions = []
                del_eff_actions = []
                for a in actions:
                    if p in a.add_effects:
                        add_eff_actions.append(a)
                    if p in a.del_effects:
                        del_eff_actions.append(a)

                ant = And(Not(self.prop_at(p, i)), self.prop_at(p, i+1))
                cons = []
                for a in add_eff_actions:
                    cons.append(self.action_prop_at(a,i))
                cons = Or(*cons)
                frame_axioms.append(Implies(ant,cons))

                ant = And(self.prop_at(p, i), Not(self.prop_at(p, i+1)))
                cons = []
                for a in del_eff_actions:
                    cons.append(self.action_prop_at(a, i))
                cons = Or(*cons)
                frame_axioms.append(Implies(ant, cons))

        s.add(s0_formula)
        s.add(goal_formula)
        s.add(And(*action_formula))
        s.add(And(*exclusion_axiom))
        s.add(And(*frame_axioms))


    def action(self,action,t):

        ant = self.action_prop_at(action,t)#TODO Add parameters when we start to deal with FOL
        precond = []
        for pred in action.positive_preconditions:
            precond.append(self.prop_at(pred,t))
        for pred in action.negative_preconditions:
            precond.append(Not(self.prop_at(pred,t)))

        effect = []
        for pred in action.add_effects:
            effect.append(self.prop_at(pred, t+1))
        for pred in action.del_effects:
            effect.append(Not(self.prop_at(pred, t+1)))

        cons = And(And(*precond),And(*effect))

        st = Implies(ant, cons)
        return st

    def action_prop_at(self,action,t):
        prop = self.prop_at((action.name,),t)
        self.action_map[prop.decl().name()] = (action,t)
        return prop

    def prop_at(self, prop, t):
        st = ""
        for term in prop:
            st+= str(term)+"_"
        key = st+str(t)
        if not self.props.has_key(key):
            p = Bool(key)
            self.props[key] = p

        return self.props[key]

# ==========================================
# Main
# ==========================================
if __name__ == '__main__':
    import sys
    domain = sys.argv[1]
    problem = sys.argv[2]
    planner = SAT_Planner()
    plan = planner.solve_file(domain, problem)
    if plan:
        print('plan:')
        for act in plan:
            print(act)
    else:
        print('No plan was found')

    ## Old code
    # def encode_formula(self, actions, initial_state, goal_state, plan_length):
    #     # Parsed data
    #     domain = Domain(actions)
    #     preds = domain.all_facts
    #     state = initial_state
    #     goal_pos = goal_state[0]
    #     goal_not = goal_state[1]
    #
    #     # Encode initial state
    #     s0_formula = ""
    #     for pred in initial_state:
    #         s0_formula+= self.prop_at(pred,0)+" "
    #     s0_formula = self.land(s0_formula)
    #
    #     # Encode goal state
    #     goal_formula = ""
    #     for pred in goal_pos:
    #         goal_formula+= self.prop_at(pred, plan_length) + " "
    #
    #     for pred in goal_not:
    #         goal_formula+= self.lnot(self.prop_at(pred, plan_length)) + " "
    #
    #     goal_formula = self.land(goal_formula)
    #
    #     pred_declaration = ""
    #     action_formula = ""
    #     exclusion_axiom = ""
    #     frame_axioms = ""
    #
    #     for i in range(0,plan_length+1):
    #         for p in preds:
    #             pred_declaration += self.z3_const(self.prop_at(p, i))
    #
    #     #encode stuff over the length of the plan
    #     for i in range(0,plan_length):
    #         action_names = []
    #         #Encode actions
    #         for action in actions:
    #             action_names.append(self.action_prop_at(action,i))
    #             action_formula+=self.action(action,i)+ " "
    #
    #         #Encode exclusion axioms
    #         for (a1,a2) in combinations(action_names,2):
    #             exclusion_axiom += self.lor("{0} {1}".format(self.lnot(a1),self.lnot(a2)) )
    #
    #
    #         #Encode frame axioms
    #         #TODO Still need to encode frame axioms
    #         for p in preds:
    #             add_eff_actions = []
    #             del_eff_actions = []
    #             for a in actions:
    #                 if p in a.add_effects:
    #                     add_eff_actions.append(a)
    #                 if p in a.del_effects:
    #                     del_eff_actions.append(a)
    #
    #             ant = self.land(self.lnot(self.prop_at(p, i)) + " " + self.prop_at(p, i+1))
    #             cons = ""
    #             for a in add_eff_actions:
    #                 cons+= self.action_prop_at(a,i)+" "
    #             if cons != "":
    #                 cons = self.lor(cons)
    #                 frame_axioms += self.limply(ant,cons)
    #
    #             ant = self.land(self.prop_at(p, i) + " " + self.lnot(self.prop_at(p, i+1)))
    #             cons = ""
    #             for a in del_eff_actions:
    #                 cons += self.action_prop_at(a, i)+" "
    #             if cons != "":
    #                 cons = self.lor(cons)
    #                 frame_axioms += self.limply(ant, cons)
    #
    #
    #
    #         # Build Z3 formulas
    #         for a in action_names:
    #             pred_declaration += self.z3_const(a)
    #
    #     st = pred_declaration+"\n"
    #     st += self.z3_assert(s0_formula) + "\n"
    #     st += self.z3_assert(goal_formula) + "\n"
    #     st += self.z3_assert(self.land(action_formula))+"\n"
    #     st += self.z3_assert(self.land(exclusion_axiom))+"\n"
    #     st += self.z3_assert(self.land(frame_axioms)) + "\n"
    #     return st
    #
    # def action(self,action,t):
    #     st = ""
    #     ant = self.action_prop_at(action,t)#TODO Add parameters when we start to deal with FOL
    #     precond = ""
    #     for pred in action.positive_preconditions:
    #         precond += self.prop_at(pred,t)+" "
    #     for pred in action.negative_preconditions:
    #         precond += self.lnot(self.prop_at(pred,t))+" "
    #
    #     effect = ""
    #     for pred in action.add_effects:
    #         effect += self.prop_at(pred, t+1) + " "
    #     for pred in action.del_effects:
    #         effect += self.lnot(self.prop_at(pred, t+1)) + " "
    #
    #     cons = self.land(self.land(precond)+" "+self.land(effect))
    #
    #     st = self.limply(ant, cons)
    #     return st
    #
    # def z3_assert(self,formula):
    #     return "(assert {0})".format(formula)
    #
    # def z3_const(self, pred):
    #     return "(declare-const {0} Bool)\n".format(pred)
    #
    # def lnot(self, formula):
    #     return "(not {0})".format(formula)
    #
    # def limply(self, antecedent, consequent):
    #     return "(implies {0} {1})".format(antecedent,consequent)
    #
    # def lor(self,formula):
    #     return "(or {0})".format(formula)
    #
    # def land(self,formula):
    #     return "(and {0})".format(formula)
    #
    # def action_prop_at(self,action,t):
    #     return self.prop_at((action.name,),t)
    #
    # def prop_at(self, prop, t):
    #     st = ""
    #     for term in prop:
    #         st+= str(term)+"_"
    #     return st+str(t)