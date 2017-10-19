import pygraphviz as pgv

from itertools import chain, combinations, permutations, product
from structures.domain import State, Action, Domain
from pddl.PDDL import PDDL_Parser

from structures.domain import powerset

import sys, getopt


def generate_state_space(ops):
    allFacts = set([fact for op in ops for fact in op.all_facts()])
    return powerset(allFacts)


def generate_graph(domain):
    G = pgv.AGraph(strict=False, directed=True)

    states = [State(set(s)) for s in domain.generate_state_space()]
    for state in states:
        G.add_node(repr(state),key=repr(state))

    for s1,s2 in product(states,repeat=2):
        # print str(s1) + " to " + str(s2)
        for op in domain.actions.values():
            #print str(op)+ " is "+("not" if not op.applicable(s1) else "")+" applicable to "+str(s2)
            if op.applicable(s1) and op.result(s1) == s2:
                # print "Adding edge from "+str(s1)+" to "+str(s2)
                G.add_edge(repr(s1),repr(s2),label=op.name)
            else:
                pass
                #print "Not adding edge from " + str(s1) + " to " + str(s2) + " using op "+op.name+(" result was "+str(op.result(s1)) if op.applicable(s1) else "")

    return G


def main(argv):
    domainfile = None
    outputfile = None
    problemfile = None
    try:
        opts, args = getopt.getopt(argv,"hd:p:o:",["domain=","problem=","ofile="])
    except getopt.GetoptError:
        print 'test.py -i <inputfile> -o <outputfile>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'test.py -i <inputfile> -o <outputfile>'
            sys.exit()
        elif opt in ("-d", "--domain"):
            domainfile = arg
        elif opt in ("-p", "--problem"):
            problemfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg
    parser = PDDL_Parser()
    if domainfile is not None:
        parser.parse_domain(domainfile)
        domain = Domain(parser.actions)
    if problemfile is not None:
        problem = parser.parse_problem(problemfile)

    G = generate_graph(domain.groundify())
    if outputfile is not None:
        G.write(outputfile)
    else:
        print G


if __name__ == "__main__":
    # main(sys.argv[1:])
    main(['-d','../examples/dinner/dinner.pddl','-o','graph.dot'])


# if __name__ == '__main__':

    # # print generate_state_space([opA,opB])
    # G = generate_graph([
    #     Action('a', [], positive_preconditions=['p'], negative_preconditions=[], add_effects=['q'], del_effects=[])
    #     , Action('b', [], positive_preconditions=['q'], negative_preconditions=[], add_effects=[], del_effects=['q'])
    #     , Action('c', [], positive_preconditions=['q'], negative_preconditions=[], add_effects=['r'], del_effects=['q'])
    #     , Action('d', [], positive_preconditions=['r'], negative_preconditions=[], add_effects=['p'], del_effects=['q'])
    #     ])
    # # print G
    # G = generate_graph([
    #     Action('a', [], positive_preconditions=['p'], negative_preconditions=[], add_effects=['q'], del_effects=[])
    #     , Action('b', [], positive_preconditions=['q'], negative_preconditions=[], add_effects=['p'], del_effects=['q'])
    #     , Action('c', [], positive_preconditions=['q'], negative_preconditions=[], add_effects=[], del_effects=['q'])
    #     # , Action('d', pre=['r'], addList=['p'], delList=['q'])
    # ])
    # G.write("graph.dot")


