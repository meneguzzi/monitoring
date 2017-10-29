import unittest

from structures.domain import Domain, Action, State, Trace
from structures.sensor import Sensor, Sensor_Parser
from pddl.PDDL import PDDL_Parser

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
 
        s = parser.parse_sensor("-((((('p',)) v (('r',))) [9] (((-((('r',)) v (-((((-(-(((-(((((-(('q',))) ^ (('r',))) [2] (((('r',)) v (('r',))) [10] (('p',)))) [3] (-(((('p',)) ^ (('p',))) v (-(('p',)))))) [10] (-(((-(('r',))) ^ ((('q',)) v (('p',)))) v (('r',)))))) ^ ((-(('p',))) [1] ((((-(('p',))) v (('p',))) [10] (('p',))) ^ (-((((('r',)) [5] (('q',))) ^ (-(('r',)))) v (('r',))))))) v ((((((-((('r',)) v (('q',)))) v ((('p',)) ^ ((('p',)) [4] (('p',))))) [9] (('p',))) ^ (('r',))) ^ (('p',))) [9] (((('r',)) v ((('q',)) v (('q',)))) [4] ((('r',)) ^ ((('q',)) ^ ((((('p',)) v (('r',))) v (('p',))) ^ (-((('q',)) ^ (('p',)))))))))))) [1] (('p',))) v ((((-(('p',))) v (('q',))) [7] ((-(-(-((-((('p',)) v (((('r',)) v (('r',))) v (('p',))))) ^ ((-(-((('p',)) v (('q',))))) v (('p',))))))) v (((-(-((-(-((('q',)) v (('q',))))) ^ ((((('r',)) v (('q',))) v (-(('r',)))) v (((('q',)) v (('q',))) ^ ((('p',)) ^ (('r',)))))))) v (-((((('q',)) [6] (-((('p',)) [4] (('r',))))) ^ (('r',))) v ((('p',)) v (-(((('q',)) [10] (('r',))) v ((('q',)) [8] (('q',))))))))) ^ (('r',))))) ^ (('q',)))) [2] (((((('r',)) v ((('r',)) ^ ((((((-((('p',)) ^ (('p',)))) v (-((('r',)) ^ (('p',))))) [1] ((('p',)) [1] (('p',)))) ^ (((((('p',)) ^ (('q',))) v (-(('p',)))) [7] ((-(('p',))) ^ ((('r',)) v (('r',))))) v (-(-(-(('p',))))))) [7] (((((('r',)) v ((('p',)) [9] (('r',)))) v ((-(('q',))) ^ (-(('p',))))) v ((((('r',)) v (('q',))) ^ (-(('q',)))) [3] (((('r',)) ^ (('r',))) ^ ((('p',)) v (('q',)))))) v (((((('q',)) v (('r',))) v (('r',))) ^ (((('r',)) ^ (('r',))) ^ ((('r',)) v (('p',))))) ^ ((-((('q',)) [10] (('p',)))) ^ ((-(('p',))) ^ (('r',))))))) [10] (-(-(-(('p',)))))))) ^ (('q',))) v (((-((('p',)) ^ ((('q',)) ^ ((((((('r',)) [2] (('q',))) v (-(('p',)))) v ((('p',)) [8] (('q',)))) ^ (('p',))) [5] (-((-((('r',)) v (('r',)))) [7] ((('p',)) [6] ((('q',)) v (('p',)))))))))) [9] ((-(((((((('p',)) v (('p',))) v ((('p',)) ^ (('r',)))) ^ ((('r',)) v (('p',)))) ^ (('p',))) [2] (((('q',)) ^ (('p',))) ^ ((('q',)) ^ ((('q',)) [10] ((('p',)) ^ (('p',))))))) [9] (('r',)))) [3] (-(-(-(((('p',)) v (((('q',)) ^ (('r',))) v ((('q',)) v (('p',))))) [10] ((('q',)) [4] (((('r',)) v (('p',))) [3] ((('r',)) [10] (('p',))))))))))) [10] (('q',)))) v (((((-((((-(('q',))) v ((((('q',)) ^ (('q',))) ^ (-(('r',)))) v ((-(('p',))) v ((('p',)) ^ (('r',)))))) [6] ((('q',)) v ((-((('r',)) ^ (('r',)))) [3] ((-(('q',))) ^ (('q',)))))) [10] ((-((('p',)) v (('p',)))) ^ (('q',))))) [7] (('q',))) [4] ((-(-(((('q',)) [6] ((((('q',)) [4] (('r',))) ^ (('q',))) ^ (((('p',)) [9] (('q',))) v (('r',))))) [10] (-((((('q',)) ^ (('r',))) [7] ((('p',)) [2] (('p',)))) ^ (('q',))))))) ^ (('q',)))) v ((((((-((((('r',)) [8] (('q',))) [10] ((('q',)) [3] (('q',)))) ^ (((('p',)) ^ (('r',))) v (-(('q',)))))) v ((-(((('p',)) ^ (('q',))) ^ ((('q',)) ^ (('r',))))) ^ ((((('p',)) [3] (('q',))) [4] (-(('p',)))) v (-(-(('p',))))))) ^ ((('p',)) v (((((('p',)) ^ (('p',))) ^ (('q',))) ^ ((-(('q',))) ^ ((('q',)) v (('p',))))) v ((-((('r',)) [10] (('q',)))) ^ (('p',)))))) [10] ((-((('r',)) [6] (('q',)))) v (((-(-((('p',)) ^ (('p',))))) v (((('r',)) [7] ((('q',)) v (('p',)))) [2] (((('p',)) ^ (('p',))) v ((('r',)) [7] (('p',)))))) ^ ((('p',)) [9] ((-((('p',)) [9] (('r',)))) [9] (-((('p',)) v (('q',))))))))) v (('p',))) ^ ((('r',)) ^ (((((('r',)) ^ (('q',))) [5] ((-(((('q',)) [1] (('p',))) [6] ((('r',)) [9] (('r',))))) ^ (('q',)))) v (('r',))) v (-((((((('q',)) v (('r',))) [3] ((('r',)) ^ (('q',)))) ^ (((('p',)) v (('q',))) [9] ((('p',)) ^ (('p',))))) v (('p',))) ^ (('p',)))))))) [1] ((-((('r',)) ^ ((((('r',)) ^ ((((('q',)) v ((('p',)) ^ (('p',)))) [4] (-((('r',)) ^ (('p',))))) v ((('p',)) v ((-(('r',))) [9] (('r',)))))) v ((-((((('q',)) v (('r',))) ^ (('p',))) ^ (-((('q',)) ^ (('r',)))))) [4] ((-(((('q',)) v (('p',))) v (('r',)))) ^ (('p',))))) v ((((((-(('q',))) v ((('q',)) v (('r',)))) v (('q',))) [9] (-(((('q',)) [5] (('p',))) [4] ((('q',)) ^ (('r',)))))) [1] ((('q',)) v ((((('q',)) v (('q',))) [8] ((('q',)) v (('q',)))) v (((('r',)) v (('q',))) [8] ((('p',)) ^ (('q',))))))) [6] (-(((-((('p',)) [1] (('p',)))) [3] (((('q',)) v (('p',))) [1] ((('p',)) ^ (('q',))))) v (-((-(('r',))) ^ ((('p',)) v (('q',))))))))))) ^ (('p',))))))))) v (((('p',)) ^ (((((-(((-((('p',)) ^ ((-((((('p',)) [9] (('r',))) v (-(('q',)))) v (((('r',)) [7] (('r',))) [7] ((('r',)) [2] (('r',)))))) [4] ((('q',)) v (((('p',)) [8] ((('p',)) ^ (('r',)))) [1] (((('r',)) [1] (('r',))) v ((('q',)) [3] (('q',))))))))) [4] (-(('q',)))) [8] (('p',)))) [8] ((-(-(((((('r',)) ^ (-(((('r',)) [2] (('r',))) v ((('r',)) [10] (('p',)))))) v ((((-(('p',))) ^ ((('r',)) [4] (('r',)))) v ((('q',)) [3] (-(('p',))))) [7] ((-(-(('r',)))) v ((-(('r',))) [3] (('q',)))))) [8] (((-(('q',))) ^ ((((('r',)) [10] (('r',))) ^ (-(('q',)))) [1] ((-(('q',))) v ((('q',)) v (('p',)))))) v (('q',)))) [5] ((('q',)) ^ (('q',)))))) [6] (-(('p',))))) ^ (((('p',)) [7] (('p',))) [9] (-(-(-((-(('p',))) [8] (((((((('q',)) ^ (('r',))) v (('r',))) ^ ((-(('r',))) [6] (('q',)))) v (((('q',)) v ((('q',)) [8] (('p',)))) [4] (('q',)))) ^ (-(('q',)))) v ((((-(-(('r',)))) [6] (((('p',)) ^ (('q',))) v ((('p',)) ^ (('r',))))) ^ (((('p',)) ^ ((('r',)) ^ (('r',)))) ^ ((('p',)) ^ ((('r',)) [3] (('p',)))))) [2] ((('q',)) [4] (-(('p',)))))))))))) [2] (((-(('r',))) ^ (-((-(('p',))) v ((((-((((('p',)) ^ (('p',))) [2] ((-(('q',))) v (('r',)))) v (((('q',)) v ((('p',)) [8] (('p',)))) ^ (-((('p',)) ^ (('q',))))))) [5] ((('q',)) [1] (((-((('q',)) [8] (('q',)))) [2] (-((('q',)) ^ (('q',))))) v (((-(('q',))) [3] ((('q',)) v (('r',)))) [3] (-(-(('r',)))))))) v ((-((('q',)) v ((-((('q',)) [2] (('p',)))) v (('p',))))) v ((('r',)) ^ ((((('p',)) [6] ((('p',)) v (('r',)))) ^ (('p',))) ^ ((((('q',)) ^ (('q',))) ^ ((('r',)) ^ (('p',)))) v (('p',))))))) ^ (('r',)))))) [5] (('p',)))) v (-(('p',))))) ^ (((('p',)) v (((-((('q',)) [8] (-(('q',))))) [2] (('p',))) v ((-((-((-(('p',))) v (('q',)))) ^ ((-(-(('r',)))) [10] ((('p',)) ^ (('q',)))))) ^ (((((-((-((-((('p',)) ^ ((('p',)) [6] (('q',))))) ^ (('q',)))) ^ (('r',)))) ^ ((((-((('q',)) ^ ((-(('p',))) [10] ((('q',)) v (('p',)))))) ^ (-(((-(('r',))) ^ ((('q',)) ^ (('r',)))) v (('q',))))) [5] ((('p',)) [5] (('r',)))) [1] ((-(-((-((('p',)) ^ (('q',)))) v ((('p',)) v (('r',)))))) v (('q',))))) ^ (-((((((((('r',)) ^ (('q',))) v (-(('r',)))) ^ (((('p',)) ^ (('p',))) ^ ((('p',)) v (('r',))))) v (((-(('r',))) ^ ((('r',)) v (('r',)))) ^ ((('r',)) ^ ((('q',)) v (('q',)))))) v (((('q',)) ^ (('r',))) ^ ((('q',)) v (-((('q',)) [3] (('q',))))))) ^ ((('q',)) [4] ((('q',)) ^ ((((('q',)) v (('r',))) [4] (('q',))) [2] (((('q',)) v (('p',))) v ((('r',)) [7] (('r',)))))))) [4] ((-((('r',)) [7] (('q',)))) [9] (-(('p',))))))) [2] ((((-(((((('p',)) [1] ((('r',)) ^ (('r',)))) [2] (-((('q',)) [1] (('r',))))) v (('p',))) [8] ((((-(('p',))) v ((('p',)) v (('r',)))) [3] (((('q',)) ^ (('q',))) [3] ((('p',)) v (('p',))))) [4] (((('p',)) [3] (-(('r',)))) ^ ((('p',)) ^ ((('p',)) [5] (('q',)))))))) [5] (('r',))) v (-((-((('r',)) ^ ((-((('q',)) ^ (('p',)))) ^ (-((('p',)) v (('r',))))))) v (-((((('r',)) [2] ((('r',)) [1] (('q',)))) [6] (((('r',)) [6] (('q',))) v (('p',)))) [9] (-((-(('q',))) ^ ((('r',)) [10] (('q',)))))))))) v (((('r',)) v (-((((((('q',)) [9] (('r',))) ^ (-(('r',)))) [1] (((('p',)) v (('q',))) v ((('p',)) ^ (('p',))))) ^ (('q',))) v (('q',))))) v ((('p',)) [2] (((((((('p',)) v (('r',))) ^ (-(('r',)))) v (((('q',)) ^ (('r',))) [8] ((('r',)) ^ (('p',))))) v (-(('q',)))) v ((-(-((('r',)) [5] (('p',))))) [7] ((((('p',)) ^ (('r',))) v ((('q',)) [6] (('p',)))) v (((('r',)) v (('r',))) ^ (('q',)))))) ^ (('r',))))))) [5] ((-((((((('r',)) v ((-((('q',)) v (('q',)))) ^ (-((('p',)) v (('p',)))))) [10] (((((('p',)) [5] (('p',))) v ((('q',)) [10] (('p',)))) ^ (-((('q',)) ^ (('q',))))) [4] ((-(-(('r',)))) [8] (('q',))))) v (-((-(-(('r',)))) [10] ((('p',)) ^ (((('q',)) [1] (('r',))) [6] ((('r',)) v (('p',)))))))) ^ ((-((((-(('r',))) [4] ((('p',)) v (('r',)))) [7] (((('r',)) v (('p',))) ^ ((('r',)) v (('p',))))) v (('r',)))) ^ (-(((-((('q',)) ^ (('q',)))) v (((('r',)) [10] (('r',))) [3] ((('p',)) v (('p',))))) ^ ((('r',)) ^ (((('p',)) ^ (('r',))) [3] ((('r',)) v (('r',))))))))) ^ ((((('r',)) ^ (((('p',)) ^ ((('r',)) ^ ((('r',)) [8] (('q',))))) v (-(((('r',)) v (('q',))) [4] (('r',)))))) v (('r',))) [9] (((-((((('r',)) ^ (('r',))) [1] ((('p',)) [2] (('q',)))) v (-(('r',))))) ^ ((((-(('q',))) v ((('r',)) [1] (('r',)))) v (-(('p',)))) v ((-((('q',)) [2] (('q',)))) ^ (((('r',)) ^ (('r',))) [6] ((('r',)) [10] (('q',))))))) [6] ((((((('r',)) ^ (('q',))) ^ (('r',))) [5] (('q',))) v ((('r',)) v (-((('q',)) ^ (('r',)))))) v ((((-(('q',))) [3] (-(('q',)))) [8] (-((('q',)) [1] (('r',))))) ^ (('p',)))))))) v (-((('p',)) [3] ((((('p',)) ^ (-(('q',)))) v (('p',))) ^ (('r',)))))))))) ^ (-(((('p',)) v (-(('r',)))) [4] (('r',))))))) [2] (('q',)))))")




if __name__ == '__main__':
    unittest.main()
