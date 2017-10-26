#!/usr/bin/env python
# Four spaces as indentation [no tabs]

import unittest
from structures.domain import Action
from pddl.propositional_planner import Propositional_Planner

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
                Action('cook', [], [['clean']], [], [['dinner']], []),
                Action('wrap', [], [['quiet']], [], [['present']], []),
                Action('carry', [], [['garbage']], [], [], [['garbage'], ['clean']])
            ]
                         )

    #-------------------------------------------
    # Split propositions
    #-------------------------------------------

if __name__ == '__main__':
    unittest.main()