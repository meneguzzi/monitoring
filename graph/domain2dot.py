import pygraphviz as pgv

from itertools import chain, combinations, permutations, product
from structures.domain import State, Action

from structures.domain import powerset


def generate_state_space(ops):
    allFacts = set([fact for op in ops for fact in op.all_facts()])
    # for op in ops:
    #     allFacts += op.allFacts()
    return powerset(allFacts)


def generate_graph(ops):
    G = pgv.AGraph(strict=False, directed=True)

    states = [State(set(s)) for s in generate_state_space(ops)]
    for state in states:
        G.add_node(repr(state),key=repr(state))

    for s1,s2 in product(states,repeat=2):
        print str(s1) + " to " + str(s2)
        for op in ops:
            # print str(op)+ " is "+("not" if not op.applicable(s1) else "")+" applicable to "+str(s2)
            if op.applicable(s1) and op.result(s1) == s2:
                # print "Adding edge from "+str(s1)+" to "+str(s2)
                G.add_edge(repr(s1),repr(s2),label=op.name)
            else:
                pass
                #print "Not adding edge from " + str(s1) + " to " + str(s2) + " using op "+op.name+(" result was "+str(op.result(s1)) if op.applicable(s1) else "")

    return G

if __name__ == '__main__':

    # print generate_state_space([opA,opB])
    G = generate_graph([
        Action('a', pre=['p'], addList=['q'], delList=[])
        ,Action('b', pre=['q'], addList=[], delList=['q'])
        ,Action('c', pre=['q'], addList=['r'], delList=['q'])
        ,Action('d', pre=['r'], addList=['p'], delList=['q'])
        ])
    # print G
    G = generate_graph([
        Action('a', pre=['p'], addList=['q'], delList=[])
        , Action('b', pre=['q'], addList=['p'], delList=['q'])
        , Action('c', pre=['q'], addList=[], delList=['q'])
        # , Action('d', pre=['r'], addList=['p'], delList=['q'])
    ])
    G.write("graph.dot")