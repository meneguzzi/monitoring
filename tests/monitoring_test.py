import unittest

from structures.domain import Domain, Action, State, Trace
from structures.sensor import Sensor, Sensor_Parser
from pddl.PDDL import PDDL_Parser
from pddl.propositional_planner import Propositional_Planner
from pddl.sat_planner import SAT_Planner
import monitoring.monitor
from monitoring.monitor import evaluate_sensor_on_traces, generate_all_traces, sample_traces
import time
import sys


class MonitoringTestCase(unittest.TestCase):

    def domain1(self):
        return Domain([Action('a', [], positive_preconditions=[('p',)], negative_preconditions=[], add_effects=[('q',)],
                              del_effects=[])
        , Action('b', [], positive_preconditions=[('q',)], negative_preconditions=[], add_effects=[], del_effects=[('q',)])
        , Action('c', [], positive_preconditions=[('q',)], negative_preconditions=[], add_effects=[('r',)], del_effects=[('q',)])
        , Action('d', [], positive_preconditions=[('r',)], negative_preconditions=[], add_effects=[('p',)], del_effects=[('q',)])
                       ])

    def test_domain1_parse(self):
        A = self.domain1()
        parser = PDDL_Parser()
        parser.parse_domain('examples/simple/simple.pddl')
        parser.parse_problem('examples/simple/pb1.pddl')
        # self.assertEquals(parser.actions,A.actions)

    def test_monitoring(self):
        A = self.domain1()
        t1 = Trace([A['a'],A['b']])
        sensor = Sensor(Sensor(('p',)),"v",Sensor(('q',)))
        state = State([('p',)])
        assert(sensor.is_model_of(t1,state))

        sensor = Sensor(Sensor(('p',)), 1, Sensor(('q',)))
        assert (sensor.is_model_of(t1, state))

    def test_sensor(self):
        sigma = Sensor(Sensor(Sensor(('p',)),"-"),"v",Sensor(('q',)))
        assert(sigma != None)
        parser = Sensor_Parser()

        print sigma

        sigma1 = parser.parse_sensor(str(sigma))
        print sigma1
        self.assertEqual(sigma, sigma1)

        sigma2 = parser.parse_sensor('((p) v (q))')
        print sigma2

        sigma3 = parser.parse_sensor('((p) [1] (q))')
        print sigma3

        sigma4 = parser.parse_sensor('(( (p) v (q) ) [1] (q) )')
        print sigma4

        s = parser.parse_sensor(str(sigma4))
        print s
        self.assertEqual(s,sigma4)

        s0 = State([])
        print str(sigma1) + " should be a model of " + str(s0)
        self.assertTrue(sigma1.is_model_of([], s0))
        self.assertFalse(sigma2.is_model_of([], s0))
        self.assertFalse(sigma3.is_model_of([], s0))
        self.assertFalse(sigma4.is_model_of([], s0))

        s1 = State([('q',)])
        print str(sigma1) + " should be a model of "+ str(s1)
        self.assertTrue(sigma1.is_model_of([],s1))
        print str(sigma2) + " should be a model of " + str(s1)
        self.assertTrue(sigma2.is_model_of([], s1))
        print str(sigma3) + " should not be a model of " + str(s1)
        self.assertFalse(sigma3.is_model_of([], s1))
        print str(sigma4) + " should be a model of " + str(s1)
        self.assertTrue(sigma4.is_model_of([], s1))

        ## Now for more complex tests (perhaps break it down)
        a1 = Action('a1', [], [], [], [('q',)], [])
        s2 = State([('p',)])
        print str(sigma3) + " should be a model of " + str(s2) + " for trace " + str([a1])
        self.assertTrue(sigma3.is_model_of([a1],s2))

    @unittest.skipUnless(sys.platform.startswith("linux"), "Only test in Travis")
    def test_evaluate_sensor_on_traces(self):
        """ test demorgan"""
        simplePDDL = 'examples/simple/simple.pddl'
        sp = Sensor_Parser()
        traces = monitoring.monitor.generate_all_traces(simplePDDL)
        print traces

        # a=evaluate_sensor_on_traces(traces,sp.parse_sensor("(-((q) v (p)))"))
        a = evaluate_sensor_on_traces(traces, sp.parse_sensor("(-((q) ^ (p)))"))
        b = evaluate_sensor_on_traces(traces, sp.parse_sensor("((-(q)) ^ (-(p)))"))
        print "Sensor a's valid traces " + str(a[0])
        print "Sensor b's valid traces " + str(b[0])
        print "Intersection between two sensors: " + str(len(set(a[0]) & set(b[0])))
        print "Valid traces for sensor a: " + str(len(set(a[0])))
        print "Valid traces for sensor b: " + str(len(set(b[0])))
        self.assertNotEqual(len(set(a[0])), len(set(b[0])))

        print "Sensor a's invalid traces " + str(a[1])
        print "Sensor b's invalid traces " + str(b[1])
        print "Intersection of invalid traces: " + str(len(set(a[1]) & set(b[1])))
        print "Invalid traces for sensor a: " + str(len(set(a[1])))
        self.assertNotEqual(len(set(a[1])), len(set(b[1])))

    def test_evaluate_temporal_sensor_on_traces(self):
        """ test demorgan"""
        simplePDDL = 'examples/simple/simple.pddl'
        sp = Sensor_Parser()
        traces = monitoring.monitor.generate_all_traces(simplePDDL)
        a = evaluate_sensor_on_traces(traces, sp.parse_sensor("((q) [2] (r))"))
        b = evaluate_sensor_on_traces(traces, sp.parse_sensor("((r) [1] (q))"))
        print "Sensor a's valid traces " + str(a[0])
        print "Sensor b's valid traces " + str(b[0])
        print "Intersection between two sensors: " + str(len(set(a[0]) & set(b[0])))
        print "Valid traces for sensor a: " + str(len(set(a[0])))
        print "Valid traces for sensor b: " + str(len(set(b[0])))
        self.assertNotEqual(len(set(a[0])),len(set(b[0])))

        print "Sensor a's invalid traces " + str(a[1])
        print "Sensor b's invalid traces " + str(b[1])
        print "Intersection of invalid traces: " + str(len(set(a[1]) & set(b[1])))
        print "Invalid traces for sensor a: " + str(len(set(a[1])))
        self.assertNotEqual(len(set(a[1])), len(set(b[1])))

    @unittest.skipUnless(sys.platform.startswith("linux"), "Only test in Travis")
    def test_evaluate_sensors_on_psr_domain(self):
        psrPDDL = 'examples/psr-small/domain01.pddl'
        sp = Sensor_Parser()
        samples = 1000
        print "Generating  {0} traces for {1}".format(samples,psrPDDL)
        # Since this domain is too large, we need to sample
        traces = monitoring.monitor.sample_traces(psrPDDL, samples)
        # traces = monitoring.monitor.generate_all_traces(psrPDDL)
        print "Generated {0} valid samples from a population of {1} states".format(len(traces),samples)
        a = evaluate_sensor_on_traces(traces, sp.parse_sensor("((NOT-UPDATED-CB1) v (UPDATED-CB1))"))
        b = evaluate_sensor_on_traces(traces, sp.parse_sensor("((NOT-UPDATED-CB1) ^ (NOT-CLOSED-CB1))"))

        print "Sensor a's valid traces " + str(a[0])
        print "Sensor b's valid traces " + str(b[0])
        print "Intersection between two sensors: " + str(len(set(a[0]) & set(b[0])))
        print "Valid traces for sensor a: " + str(len(set(a[0])))
        print "Valid traces for sensor b: " + str(len(set(b[0])))
        self.assertNotEqual(len(set(a[0])), len(set(b[0])))

        print "Sensor a's invalid traces " + str(a[1])
        print "Sensor b's invalid traces " + str(b[1])
        print "Intersection of invalid traces: " + str(len(set(a[1]) & set(b[1])))
        print "Invalid traces for sensor a: " + str(len(set(a[1])))
        self.assertNotEqual(len(set(a[1])), len(set(b[1])))

    @unittest.skipUnless(sys.platform.startswith("linux"), "Only test in Travis")
    def test_generate_all_traces(self):
        simplePDDL = 'examples/simple/simple.pddl'

        start = time.time()
        generate_all_traces(simplePDDL,Propositional_Planner())
        end = time.time()
        print "Search planner took {0}s to generate traces".format(end - start)

        # SAT is much slower, so no need to waste testing time here
        # start = time.time()
        # generate_all_traces(simplePDDL, SAT_Planner())
        # end = time.time()
        # print "SAT planner took {0}s to generate traces".format(end - start)

    @unittest.skipUnless(sys.platform.startswith("linux"), "Only test in Travis")
    def test_sample_traces(self):
        pddl_file = 'examples/simple/simple.pddl'

        start = time.time()
        sample_traces(pddl_file,100)
        end = time.time()
        print "Trace sample took {0}s for {1}".format(end - start, pddl_file)

        pddl_file = 'examples/psr-small/domain01.pddl'
        start = time.time()
        sample_traces(pddl_file,100)
        end = time.time()
        print "Trace sample took {0}s for {1}".format(end - start, pddl_file)


if __name__ == '__main__':
    unittest.main()
