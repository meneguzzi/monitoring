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
        s = Sensor(Sensor(Sensor("p"),"-"),"v",Sensor("q"))
        assert(s != None)
        parser = Sensor_Parser()

        print s 

        s1=parser.parse_sensor(str(s))
        print s1

        s2 = parser.parse_sensor("(p v q)")
        print s2

        s = parser.parse_sensor("(p [1] q)")
        print s

        s = parser.parse_sensor("((p v q) [1] q)")
        print s
        s = parser.parse_sensor(str(s))
        print s
 
    def test_evaluate_sensor(self):
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

    def test_evaluate_temporal_sensor(self):
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
