#!/usr/bin/env python
# Four spaces as indentation [no tabs]

import unittest
from structures.domain import Action
from pddl.PDDL import PDDL_Parser, PDDL_Planner

# ==========================================
# Test PDDL
# ==========================================

class PDDL_Test(unittest.TestCase):

    # ------------------------------------------
    # Test scan_tokens
    # ------------------------------------------

    def test_scan_tokens_domain(self):
        parser = PDDL_Parser()
        self.assertEqual(parser.scan_tokens('examples/dinner/dinner.pddl'),
            ['define', ['domain', 'dinner'],
            [':requirements', ':strips'],
            [':predicates', ['clean'], ['dinner'], ['quiet'], ['present'], ['garbage']],
            [':action', 'cook',
                ':parameters', [],
                ':precondition', ['and', ['clean']],
                ':effect', ['and', ['dinner']]],
            [':action', 'wrap',
                ':parameters', [],
                ':precondition', ['and', ['quiet']],
                ':effect', ['and', ['present']]],
            [':action', 'carry',
                ':parameters', [],
                ':precondition', ['and', ['garbage']],
                ':effect', ['and', ['not', ['garbage']], ['not', ['clean']]]],
            [':action', 'dolly',
                ':parameters', [],
                ':precondition', ['and', ['garbage']],
                ':effect', ['and', ['not', ['garbage']], ['not', ['quiet']]]]]
        )

    def test_scan_tokens_problem(self):
        parser = PDDL_Parser()
        self.assertEqual(parser.scan_tokens('examples/dinner/pb1.pddl'),
            ['define', ['problem', 'pb1'],
            [':domain', 'dinner'],
            [':init', ['garbage'], ['clean'], ['quiet']],
            [':goal', ['and', ['dinner'], ['present'], ['not', ['garbage']]]]]
        )

    # ------------------------------------------
    # Test parse domain
    # ------------------------------------------

    def test_parse_domain(self):
        parser = PDDL_Parser()
        parser.parse_domain('examples/dinner/dinner.pddl')
        print parser.actions
        self.assertEqual(parser.domain_name, 'dinner')
        self.assertEqual(parser.actions,
            [
                Action('cook', [], [('clean',)], [], [('dinner',)], []),
                Action('wrap', [], [('quiet',)], [], [('present',)], []),
                Action('carry', [], [('garbage',)], [], [], [('garbage',), ('clean',)]),
                Action('dolly', [], [('garbage',)], [], [], [('garbage',), ('quiet',)])
            ]
        )

    # ------------------------------------------
    # Test parse problem
    # ------------------------------------------

    def test_parse_problem(self):
        parser = PDDL_Parser()
        parser.parse_domain('examples/dinner/dinner.pddl')
        parser.parse_problem('examples/dinner/pb1.pddl')
        self.assertEqual(parser.problem_name, 'pb1')
        self.assertEqual(parser.objects, [])
        self.assertEqual(parser.state, [('garbage',),('clean',),('quiet',)])
        self.assertEqual(parser.positive_goals, [('dinner',), ('present',)])
        self.assertEqual(parser.negative_goals, [('garbage',)])

    #-------------------------------------------
    # Split propositions
    #-------------------------------------------

    def test_parse_first_order(self):
        parser = PDDL_Parser()
        parser.parse_domain('examples/dwr/dwr.pddl')
        parser.parse_problem('examples/dwr/pb1.pddl')
        self.assertEqual(parser.problem_name, 'pb1')
        # self.assertEqual(parser.objects, ['r1','l1','l2','k1','k2','p1','q1','p2','q2','ca','cb','cc','cd','ce','cf', 'pallet'])
        print parser.actions
        # self.assertEqual(parser.state, [['garbage'], ['clean'], ['quiet']])
        # self.assertEqual(parser.positive_goals, [['dinner'], ['present']])
        # self.assertEqual(parser.negative_goals, [['garbage']])

    def test_reachability_analysis(self):
        parser = PDDL_Parser()
        parser.parse_domain('examples/dinner/dinner.pddl')
        parser.parse_problem('examples/dinner/pb1.pddl')
        planner = PDDL_Planner()
        self.assertTrue(planner.solvable(parser.domain,parser.initial_state,parser.goal))
        initial_state = [p for p in parser.initial_state]
        initial_state.remove(("clean",))
        self.assertFalse(planner.solvable(parser.domain,initial_state,parser.goal))
        domain = [a for a in parser.domain]
        domain.pop(0)
        self.assertFalse(planner.solvable(domain, initial_state, parser.goal))

if __name__ == '__main__':
    unittest.main()