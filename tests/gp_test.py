import unittest

import monitoring.monitor
from gp.gpOps import GPOps
from gp.nodeGenerator import NodeGenerator
from gp.population import Population
from monitoring.monitor import evaluate_sensor_on_traces
from pddl.PDDL import PDDL_Parser
from structures.sensor import Sensor, Sensor_Parser
from graph import domain2dot
import sys


class GPTestCase(unittest.TestCase):

    @unittest.skipUnless(sys.platform.startswith("linux"), "Only test in Travis")
    def test_randomsensor(self):
        parser = PDDL_Parser()
        simplePDDL = 'examples/simple/simple.pddl'
        parser.parse_domain(simplePDDL)
        parser.parse_problem('examples/simple/pb1.pddl')
        domain = parser.domain.groundify()
        terms = []
        for i in range(0, 5):
            terms.append(Sensor.generate_sensor(domain, 5))
        ng = NodeGenerator(terms, 1, 2, 2, 4)
        traces = monitoring.monitor.generate_all_traces(simplePDDL)
        sp = Sensor_Parser()
        gpo = GPOps(terms, 1, 5, 1, 4)
        pop = Population(100, ng, 0.8, 0.05, 0.1, gpo, sp.parse_sensor("(p v q)"), traces)
        # for i in range(0,100):
        #         pop.generation()
        # print pop.generation()


    def test_randomsensor_large(self):
        parser = PDDL_Parser()
        pddl = 'examples/psr-small/domain01.pddl'
        parser.parse_domain(pddl)
        parser.parse_problem('examples/psr-small/task01.pddl')
        domain = parser.domain.groundify()
        terms = []
        for i in range(0, 5):
            terms.append(Sensor.generate_sensor(domain, 5))
        ng = NodeGenerator(terms, 1, 2, 2, 4)
        samples = 1000
        print "Sampling {0} traces from the domain".format(samples)
        traces = monitoring.monitor.sample_traces(pddl,1000)
        print "Generated {0} valid traces from a sample of {1}".format(len(traces),samples)
        sp = Sensor_Parser()
        gpo = GPOps(terms, 1, 5, 1, 4)
        pop = Population(100, ng, 0.8, 0.05, 0.1, gpo, sp.parse_sensor("((NOT-UPDATED-CB1) v (UPDATED-CB1))"), traces)


if __name__ == '__main__':
    unittest.main()
