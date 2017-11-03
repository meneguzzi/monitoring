import unittest

from structures.domain import Domain, Action, State, Trace
from structures.sensor import Sensor, Sensor_Parser
from pddl.PDDL import PDDL_Parser
import monitoring.monitor
from monitoring.monitor import evaluate_sensor_on_traces

class MonitoringTestCase(unittest.TestCase):

    def domain1(self):
        return Domain([Action('a', [], positive_preconditions=['p'], negative_preconditions=[], add_effects=['q'],
                              del_effects=[])
        , Action('b', [], positive_preconditions=['q'], negative_preconditions=[], add_effects=[], del_effects=['q'])
        , Action('c', [], positive_preconditions=['q'], negative_preconditions=[], add_effects=['r'], del_effects=['q'])
        , Action('d', [], positive_preconditions=['r'], negative_preconditions=[], add_effects=['p'], del_effects=['q'])
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
        sensor = Sensor(Sensor("p"),"v",Sensor("q"))
        state = State(["p"])
        assert(sensor.is_model_of(t1,state))

        sensor = Sensor(Sensor("p"), 1, Sensor("q"))
        assert (sensor.is_model_of(t1, state))

    def test_sensor(self):
        sigma = Sensor(Sensor(Sensor("p"),"-"),"v",Sensor("q"))
        assert(sigma != None)
        parser = Sensor_Parser()

        print sigma

        sigma1 = parser.parse_sensor(str(sigma))
        print sigma1

        sigma2 = parser.parse_sensor("(p v q)")
        print sigma2

        sigma3 = parser.parse_sensor("(p [1] q)")
        print sigma3

        sigma4 = parser.parse_sensor("((p v q) [1] q)")
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

        s1 = State(['q'])
        print str(sigma1) + " should be a model of "+ str(s1)
        self.assertTrue(sigma1.is_model_of([],s1))
        print str(sigma2) + " should be a model of " + str(s1)
        self.assertTrue(sigma2.is_model_of([], s1))
        print str(sigma3) + " should not be a model of " + str(s1)
        self.assertFalse(sigma3.is_model_of([], s1))
        print str(sigma4) + " should be a model of " + str(s1)
        self.assertTrue(sigma4.is_model_of([], s1))

        ## Now for more complex tests (perhaps break it down)
        a1 = Action('a1', [], [], [], ['q'], [])
        s2 = State(['p'])
        print str(sigma3) + " should be a model of " + str(s2) + " for trace " + str([a1])
        self.assertTrue(sigma3.is_model_of([a1],s2))

 
    def test_evaluate_sensor_on_traces(self):
        """ test demorgan"""
        simplePDDL = 'examples/simple/simple.pddl'
        sp = Sensor_Parser()
        traces = monitoring.monitor.generate_all_traces(simplePDDL)

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
        a = evaluate_sensor_on_traces(traces, sp.parse_sensor("(q [2] r)"))
        b = evaluate_sensor_on_traces(traces, sp.parse_sensor("(r [1] q)"))
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



if __name__ == '__main__':
    unittest.main()
