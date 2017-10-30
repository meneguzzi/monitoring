import unittest

from structures.domain import Domain, Action, State, Trace
from structures.sensor import Sensor, Sensor_Parser
from pddl.PDDL import PDDL_Parser
from gp.nodeGenerator import NodeGenerator


class GPTestCase(unittest.TestCase):

    def test_randomsensor(self):
        parser=PDDL_Parser()
        parser.parse_domain('examples/simple/simple.pddl')
        parser.parse_problem('examples/simple/pb1.pddl')
        domain = parser.domain.groundify()
        terms=[]
        for i in range(0,5):
          terms.append(Sensor.generate_sensor(domain, 5))
        ng=NodeGenerator(terms,1,2,2,4)
        r=ng.addNode(None,0)
        print(r.compile())


if __name__ == '__main__':
    unittest.main()
