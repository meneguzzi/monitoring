import unittest

from structures.domain import Domain, Action, State, Trace
from structures.sensor import Sensor


class MonitoringTestCase(unittest.TestCase):

    def domain1(self):
        return Domain([Action('a', pre=['p'], addList=['q'], delList=[])
        ,Action('b', pre=['q'], addList=[], delList=['q'])
        ,Action('c', pre=['q'], addList=['r'], delList=['q'])
        ,Action('d', pre=['r'], addList=['p'], delList=['q'])
        ])

    def test_monitoring(self):
        A = self.domain1()
        t1 = Trace([A['a'],A['b']])
        sensor = Sensor(Sensor("p"),"v",Sensor("q"))
        state = State(["p"])
        assert(sensor.is_model_of(t1,state,A))

        sensor = Sensor(Sensor("p"), 1, Sensor("q"))
        assert (sensor.is_model_of(t1, state, A))

        # self.assertEqual(True, False)
        pass

    def test_sensor(self):
        s = Sensor(Sensor("p"),"v",Sensor("q"))
        assert(s != None)



if __name__ == '__main__':
    unittest.main()
