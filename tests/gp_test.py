import unittest

from structures.domain import Domain, Action, State, Trace
from structures.sensor import Sensor, Sensor_Parser
from pddl.PDDL import PDDL_Parser


class GPTestCase(unittest.TestCase):

    def test_randomsensor(self):
        parser = PDDL_Parser()
        parser.parse_domain('examples/simple/simple.pddl')
        parser.parse_problem('examples/simple/pb1.pddl')
        domain = parser.domain.groundify()
        print Sensor.generate_sensor(domain, 5)


if __name__ == '__main__':
    unittest.main()
