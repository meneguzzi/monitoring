import unittest
from gp_test import GPTestCase
from monitoring_test import MonitoringTestCase
from PDDL_test import PDDL_Test
from propositional_planner_test import Propositional_Planner_Test

if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(GPTestCase())
    suite.addTest(MonitoringTestCase())
    suite.addTest(PDDL_Test())
    suite.addTest(Propositional_Planner_Test())
    runner = unittest.TextTestRunner()
    runner.run(suite)

