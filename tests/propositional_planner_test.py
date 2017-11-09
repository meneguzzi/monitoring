#!/usr/bin/env python
# Four spaces as indentation [no tabs]

import unittest
from structures.domain import Action
from pddl.propositional_planner import Propositional_Planner
from pddl.sat_planner import SAT_Planner

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


    def test_solve_sat(self):
        planner = SAT_Planner()
        self.assertIsNotNone(planner.solve_file('examples/dinner/dinner.pddl', 'examples/dinner/pb1.pddl'))
    #-------------------------------------------
    # Split propositions
    #-------------------------------------------

if __name__ == '__main__':
    unittest.main()