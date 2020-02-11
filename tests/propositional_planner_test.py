#!/usr/bin/env python
# Four spaces as indentation [no tabs]

import unittest
from structures.domain import Action
from pddl.propositional_planner import Propositional_Planner
from pddl.sat_planner import SAT_Planner
from pddl.heuristic_planner import Heuristic_Planner
import sys
import time

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

    # @unittest.skipUnless(sys.platform.startswith("osx"), "Skip, as travis will timeout")
    # @unittest.skip("Skip, to avoid timeout")
    def test_solve_psr(self):
        domain_template = 'examples/psr-small/domain{0}.pddl'
        problem_template = 'examples/psr-small/task{0}.pddl'
        planner = Propositional_Planner(time_limit=0.1)
        last_domain = 50
        # last_domain = 14
        for i in range(1, last_domain+1):
            domain_filename = 'examples/psr-small/domain{0}.pddl'.format("%02d" % i)
            problem_filename = 'examples/psr-small/task{0}.pddl'.format("%02d" % i)
            print "Processing ", domain_filename, " and ", problem_filename
            start = time.time()
            plan = planner.solve_file(domain_filename,problem_filename)
            end = time.time()
            print "Planning took {0}s for {1} using {2}".format(end - start, problem_filename, planner.__class__.__name__)
            print "Plan length ",len(plan) if plan is not None else 0

    def test_solve_heuristic(self):
        planner = Heuristic_Planner()
        plan = planner.solve_file('examples/dinner/dinner.pddl', 'examples/dinner/pb1.pddl')
        self.assertIsNotNone(plan)
        self.assertEqual(3, len(plan))
        # print "Plan: ", plan
        self.assertEqual(plan,
                         [
                             Action('cook', [], [('clean',)], [], [('dinner',)], []),
                             Action('carry', [], [('garbage',)], [], [], [('garbage',), ('clean',)]),
                             Action('wrap', [], [('quiet',)], [], [('present',)], [])
                         ]
                         )

    #@unittest.skipUnless(sys.platform.startswith("osx"), "Skip, since travis does not like z3")
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