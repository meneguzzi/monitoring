#!/usr/bin/env python
# Four spaces as indentation [no tabs]

import unittest
from structures.domain import Action
from pddl.propositional_planner import Propositional_Planner
from pddl.sat_planner import SAT_Planner
import sys

# ==========================================
# Test Propositional_Planner
# ==========================================

class Propositional_Planner_Test(unittest.TestCase):

    # ------------------------------------------
    # Test solve
    # ------------------------------------------

    def test_solve_dinner(self):
        planner = Propositional_Planner()
        self.assertEqual(planner.solve_file('examples/dinner/dinner.pddl', 'examples/dinner/pb1.pddl'),
                         [
                Action('cook', [], [('clean',)], [], [('dinner',)], []),
                Action('wrap', [], [('quiet',)], [], [('present',)], []),
                Action('carry', [], [('garbage',)], [], [], [('garbage',), ('clean',)])
            ]
                         )

    def test_solve_psr(self):
        domain_template = 'examples/psr-small/domain{0}.pddl'
        problem_template = 'examples/psr-small/task{0}.pddl'
        planner = Propositional_Planner()
        for i in range(1, 51):
            domain_filename = 'examples/psr-small/domain{0}.pddl'.format("%02d" % i)
            problem_filename = 'examples/psr-small/task{0}.pddl'.format("%02d" % i)
            print "Processing ", domain_filename, " and ", problem_filename
            plan = planner.solve_file(domain_filename,problem_filename)
            print "Plan length ",len(plan)


    @unittest.skipUnless(sys.platform.startswith("osx"), "Skip, since travis does not like z3")
    def test_solve_sat(self):
        planner = SAT_Planner()
        plan = planner.solve_file('examples/dinner/dinner.pddl', 'examples/dinner/pb1.pddl')
        self.assertIsNotNone(plan)
        self.assertEqual(3,len(plan))
        # print plan
        self.assertEqual(plan,
            [ Action('wrap', [], [('quiet',)],[],[('present',)],[]),
              Action('dolly', [], [('garbage',)],[],[],[('garbage',), ('quiet',)]),
              Action('cook', [], [('clean',)],[],[('dinner',)],[])]

        )

    def test_benchmark_planners(self):
        pass

if __name__ == '__main__':
    unittest.main()