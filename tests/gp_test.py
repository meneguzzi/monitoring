import sys
import unittest

import monitoring.monitor
from gp.gp import GP, sensor_for_action
from gp.gpOps import GPOps
from gp.nodeGenerator import NodeGenerator
from gp.population import Population
from pddl.PDDL import PDDL_Parser
from structures.sensor import Sensor, Sensor_Parser


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

    @unittest.skipUnless(sys.platform.startswith("linux"), "Only test in Travis")
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

    #@unittest.skipUnless(sys.platform.startswith("linux"), "Only test in Travis")
    def test_new_gp_small(self):
        gp = GP(False)
        (tpr, tnr, fpr, fnr) = gp.build_sensor_for_domain('examples/simple/simple.pddl',
                                                          "((p) v (q))", 1000)
        self.assertGreater(tpr, 0.7)

    # @unittest.skipUnless(sys.platform.startswith("linux"), "Only test in Travis")
    @unittest.skip("Overlong test")
    def test_new_gp_large(self):
        gp = GP(False)
        (tpr,tnr,fpr,fnr) = gp.build_sensor_for_domain('examples/psr-small/domain01.pddl', "((NOT-UPDATED-CB1) v (UPDATED-CB1))", 1000)
        self.assertGreater(tpr,0.9)

    def test_sensor_for_action(self):
        parser = PDDL_Parser()
        pddl = 'examples/psr-small/domain01.pddl'
        parser.parse_domain(pddl)

        s = sensor_for_action(parser.actions[0])
        self.assertIsNotNone(s)

        print "Action: ",parser.actions[0]
        print "Sensor: ",s

if __name__ == '__main__':
    unittest.main()
