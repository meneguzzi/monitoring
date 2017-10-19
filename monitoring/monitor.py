from pddl.PDDL import PDDL_Parser
from pddl.propositional_planner import Propositional_Planner
from structures.domain import State,Trace
from structures.sensor import Sensor, Sensor_Parser
from itertools import product

class MonitorSynthesizer():

    def __init__(self):
        pass


def generate_all_traces(domainfile):
    traces = set([])
    parser = PDDL_Parser()
    parser.parse_domain(domainfile)
    for s0, sg in product(domain.generate_state_space(), repeat=2):
        s0 = list(s0)
        sg = list(sg)
        plan = planner.solve(parser.domain.groundify().actions.values(),s0,(sg,[]))
        if plan is not None:
            traces.add((s0,plan))
        else:
            pass
            #print "No plan between "+str(s0)+" and "+str(sg)
    return traces


def evaluate_sensor_on_traces(traces,sensor):
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

if __name__ == '__main__':
    parser = PDDL_Parser()
    parser.parse_domain("../examples/dinner/dinner.pddl")
    parser.parse_problem("../examples/dinner/pb1.pddl")
    sensor_parser = Sensor_Parser()
    sensor = sensor_parser.parse_sensor("( (clean) [1] (dinner) )")

    domain = parser.domain.groundify()
    planner = Propositional_Planner()

    for s0, sg in product(domain.generate_state_space(), repeat=2):
        s0 = list(s0)
        sg = list(sg)
        plan = planner.solve(parser.domain.groundify().actions.values(),s0,(sg,[]))
        if plan is not None:
            if len(plan) > 0:
                print "Plan from "+str(s0)+" to "+str(sg)+" is "+str(plan)
            #t = Trace.plan_to_trace(s0,plan)
            #t.models(sensor,State(s0),domain)
            if sensor.is_model_of(plan,State(s0),domain):
                print str(sensor)+" is a model of "+str(plan)
        else:
            pass
            #print "No plan between "+str(s0)+" and "+str(sg)
