import unittest

from structures.domain import Domain, Action, State, Trace
from structures.sensor import Sensor


class MonitoringTestCase(unittest.TestCase):

    def domain1(self):
        return Domain([Action('a', [], positive_preconditions=['p'], negative_preconditions=[], add_effects=['q'],
                              del_effects=[])
        , Action('b', [], positive_preconditions=['q'], negative_preconditions=[], add_effects=[], del_effects=['q'])
        , Action('c', [], positive_preconditions=['q'], negative_preconditions=[], add_effects=['r'], del_effects=['q'])
        , Action('d', [], positive_preconditions=['r'], negative_preconditions=[], add_effects=['p'], del_effects=['q'])
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
