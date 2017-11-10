from structures.domain import Domain, Action, State, Trace
from structures.sensor import Sensor, Sensor_Parser
import structures.sensor
from pddl.PDDL import PDDL_Parser
from gp.nodeGenerator import NodeGenerator
from gp.population import Population
from gp.gpOps import GPOps
from gp.node import Node
import monitoring.monitor
from monitoring.monitor import evaluate_sensor_on_traces
import random


def test_randomsensor():
    # random.seed(149)
    parser = PDDL_Parser()
    pddl = 'examples/simple/simple.pddl'
    parser.parse_domain(pddl)
    parser.parse_problem('examples/simple/pb1.pddl')
    domain = parser.domain.groundify()
    terms = []
    for i in range(0, 15):
        terms.append(Sensor.generate_sensor(domain, 1))
    print terms
    # terms=[Sensor(("q",)),Sensor(("p",))]
    # print terms
    ng = NodeGenerator(terms, 1, 5, 2, 5)

    traces = monitoring.monitor.generate_all_traces(pddl)
    # generate a dummy node
    # root=Node(None,None,1)
    # child=Node(root,structures.sensor.sor,2)
    # root.setChild(0,child)
    # gc1=Node(child,terms[0],0)
    # gc2=Node(child,terms[1],0)
    # child.setChild(0,gc1)
    # child.setChild(1,gc2)
    # print root.compile()

    sp = Sensor_Parser()
    gpo = GPOps(terms, 1, 5, 1, 4)

    pop = Population(100, ng, 0.8, 0.05, 0.1, gpo, sp.parse_sensor("(p v q)"), traces)
    # pop.pop[0]=root
    # pop.pop[0]=root #assign manually generated node
    # and deal with it manually
    # d = evaluate_sensor_on_traces(traces,sp.parse_sensor("((p) v (q))"))
    # a = evaluate_sensor_on_traces(traces, sp.parse_sensor("((p) v (q))"))
    # a=evaluate_sensor_on_traces(traces,root.compile())
    # tp=set(d[0]) & set(a[0])
    # tn=set(d[1]) & set(a[1])
    # fp=set(a[0]) & set(d[1])
    # fn=set(a[1]) & set(d[0])
    # print len(tp)
    # print len(fp)
    # print len(tn)
    # print len(fn)
    # print len(tp)+len(tn)-len(fp)-len(fn)
    # print d[0]
    # print a[0]
    # print len(fp)


    for i in range(0, 100):
        print "g", i
        f = pop.generation()
        m = 0
        p = None
        for k, v in f.iteritems():
            if v > m:
                m = v
                p = k
                #                       print p.compile()
        if m > 0:
            print m, p.compile()
        pop.updateGen(f)

    m = 0
    p = None
    for k, v in pop.generation().iteritems():
        if v > m:
            m = v
            p = k
    d = evaluate_sensor_on_traces(traces, sp.parse_sensor("((p) v (q))"))
    a = evaluate_sensor_on_traces(traces, p.compile())
    tp = set(d[0]) & set(a[0])
    tn = set(d[1]) & set(a[1])
    fp = set(a[0]) & set(d[1])
    fn = set(a[1]) & set(d[0])
    print len(tp)
    print len(fp)
    print len(tn)
    print len(fn)
    print len(tp) + len(tn) - len(fp) - len(fn)


def test_randomsensor_psr():
    # random.seed(149)
    parser = PDDL_Parser()
    pddl = 'examples/psr-small/domain01.pddl'
    parser.parse_domain(pddl)
    parser.parse_problem('examples/psr-small/task01.pddl')
    domain = parser.domain.groundify()
    terms = []
    for i in range(0, 15):
        terms.append(Sensor.generate_sensor(domain, 1))
    print terms
    # terms=[Sensor(("q",)),Sensor(("p",))]
    # print terms
    ng = NodeGenerator(terms, 1, 5, 2, 5)

    samples = 1000
    print "Sampling {0} traces from the domain".format(samples)
    traces = monitoring.monitor.sample_traces(pddl, 1000)
    print "Generated {0} valid traces from a sample of {1}".format(len(traces), samples)

    sp = Sensor_Parser()
    gpo = GPOps(terms, 1, 5, 1, 4)

    pop = Population(100, ng, 0.8, 0.05, 0.1, gpo, sp.parse_sensor("((NOT-UPDATED-CB1) v (UPDATED-CB1))"), traces)

    for i in range(0, 100):
        print "g", i
        f = pop.generation()
        m = 0
        p = None
        for k, v in f.iteritems():
            if v > m:
                m = v
                p = k
                #                       print p.compile()
        if m > 0:
            print m, p.compile()
        pop.updateGen(f)

    m = 0
    p = None
    for k, v in pop.generation().iteritems():
        if v > m:
            m = v
            p = k
    d = evaluate_sensor_on_traces(traces, sp.parse_sensor("((NOT-UPDATED-CB1) v (UPDATED-CB1))"))
    a = evaluate_sensor_on_traces(traces, p.compile())
    tp = set(d[0]) & set(a[0])
    tn = set(d[1]) & set(a[1])
    fp = set(a[0]) & set(d[1])
    fn = set(a[1]) & set(d[0])
    print len(tp)
    print len(fp)
    print len(tn)
    print len(fn)
    print len(tp) + len(tn) - len(fp) - len(fn)


if __name__ == '__main__':
    # test_randomsensor()
    test_randomsensor_psr()
