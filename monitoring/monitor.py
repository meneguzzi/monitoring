from pddl.PDDL import PDDL_Parser, PDDL_Planner
from pddl.propositional_planner import Propositional_Planner
from structures.domain import State,Trace, Domain
from structures.sensor import Sensor, Sensor_Parser
from itertools import product, permutations

import random

class MonitorSynthesizer():

    def __init__(self):
        pass

def get_domain(domain_file):
    pddlparser = PDDL_Parser()
    pddlparser.parse_domain(domain_file)
    pdomain = pddlparser.domain.groundify()
    return pdomain

def generate_traces_for_population(domain,population,ignore_empty,planner):
    traces = []
    for s0, sg in population:
        if planner.solvable(domain, s0, (sg, [])):
            plan = planner.solve(domain, s0, (sg, []))
            if plan is not None:
                traces.append((s0, tuple(plan), sg))
    return traces


def sample_traces(domain_file, max_samples=100, ignore_empty = True, planner = Propositional_Planner()):
    traces = []
    domain = get_domain(domain_file)

    population = [(s0,sg) for s0, sg in permutations(domain.state_space, 2)]
    max_samples = min(len(population),max_samples)
    population = random.sample(population, max_samples)
    return generate_traces_for_population(domain,population,ignore_empty,planner)
    # traces = []
    # for s0, sg in population:
    #     if planner.solvable(domain,s0,(sg,[])):
    #         plan = planner.solve(domain,s0, (sg, []) )
    #         if plan is not None:
    #             traces.append((s0,tuple(plan),sg))
    # return traces

def generate_all_traces(domain_file, planner = Propositional_Planner()):
    traces = []
    domain = get_domain(domain_file)
    for s0, sg in product(domain.generate_state_space(), repeat=2):
        s0l = list(s0)
        sgl = list(sg)
        if planner.solvable(domain,s0l,(sgl,[])):
            plan = planner.solve(domain.actions.values(),s0l,(sgl,[]))
            if plan is not None:
                traces.append((s0,tuple(plan),sg))
        else:
            pass
            #print "No plan between "+str(s0)+" and "+str(sg)
    return traces


def evaluate_sensor_on_traces(traces,sensor):
    assert isinstance(sensor, Sensor)
    valid = []
    invalid = []
    for t in traces:
        s0 = t[0]
        plan = t[1]
        if sensor.is_model_of(plan,State(s0)):
            valid.append(t)
        else:
            invalid.append(t)
    return (valid,invalid)

# if __name__ == '__main__':
#     parser = PDDL_Parser()
#     parser.parse_domain("../examples/dinner/dinner.pddl")
#     parser.parse_problem("../examples/dinner/pb1.pddl")
#     sensor_parser = Sensor_Parser()
#     sensor = sensor_parser.parse_sensor("( (clean) [1] (dinner) )")
#
#     domain = parser.domain.groundify()
#     planner = Propositional_Planner()
#
#     for s0, sg in product(domain.generate_state_space(), repeat=2):
#         s0 = list(s0)
#         sg = list(sg)
#         plan = planner.solve(parser.domain.groundify().actions.values(),s0,(sg,[]))
#         if plan is not None:
#             if len(plan) > 0:
#                 print "Plan from "+str(s0)+" to "+str(sg)+" is "+str(plan)
#             #t = Trace.plan_to_trace(s0,plan)
#             #t.models(sensor,State(s0),domain)
#             if sensor.is_model_of(plan,State(s0),domain):
#                 print str(sensor)+" is a model of "+str(plan)
#         else:
#             pass
#             #print "No plan between "+str(s0)+" and "+str(sg)
