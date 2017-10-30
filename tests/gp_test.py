import unittest

from structures.domain import Domain, Action, State, Trace
from structures.sensor import Sensor, Sensor_Parser
from pddl.PDDL import PDDL_Parser
from gp.nodeGenerator import NodeGenerator
from gp.population import Population
from gp.gpOps import GPOps
import monitoring.monitor
from monitoring.monitor import evaluate_sensor_on_traces


class GPTestCase(unittest.TestCase):

   def test_evaluate_sensor(self):
        """ test demorgan"""
        simplePDDL='examples/simple/simple.pddl'
        sp=Sensor_Parser()
        traces=monitoring.monitor.generate_all_traces(simplePDDL)
        #a=evaluate_sensor_on_traces(traces,sp.parse_sensor("(-((q) v (p)))"))
        a=evaluate_sensor_on_traces(traces,sp.parse_sensor("(-((q) ^ (p)))"))
        b=evaluate_sensor_on_traces(traces,sp.parse_sensor("((-(q)) ^ (-(p)))"))
        print len(set(a[0]) & set(b[0]))
        print len(set(a[0]))
        print len(set(b[0]))
        print len(set(a[1]) & set(b[1]))
        print len(set(a[1]))

   def test_randomsensor(self):
        parser=PDDL_Parser()
        simplePDDL='examples/simple/simple.pddl'
        parser.parse_domain(simplePDDL)
        parser.parse_problem('examples/simple/pb1.pddl')
        domain = parser.domain.groundify()
        terms=[]
        for i in range(0,5):
          terms.append(Sensor.generate_sensor(domain, 5))
        ng=NodeGenerator(terms,1,2,2,4)

        traces=monitoring.monitor.generate_all_traces(simplePDDL)

        sp=Sensor_Parser()
        gpo=GPOps(terms,1,5,1,4)

        pop=Population(100,ng,0.8,0.05,0.1,gpo,sp.parse_sensor("(p v q)"),traces)

    #    for i in range(0,100):
    #            pop.generation()
    #    print pop.generation()


        


if __name__ == '__main__':
    unittest.main()
