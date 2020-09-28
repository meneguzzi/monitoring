import numpy as np
from copy import copy
from node import Node
from structures.sensor import * 
from pprint import pprint
import random
import time

class Environment():
    
    def __init__(self, ng, modelSensor, traces, ms):
        # Nir's stuff
        self.traces = traces
        self.modelSensor = modelSensor
        self.ng = ng
        self.ms = ms

        # Persistent stuff
        self.desired = self.ms.evaluate_sensor_on_traces(self.traces, self.modelSensor)
        self.min_depth = self.ng.minDepth
        self.max_depth = self.ng.maxDepth
        self.min_path = self.ng.minSpath
        self.max_path = self.ng.maxSpath
        self.paths = range(self.min_path, self.max_path+1)
        self.operators = ['and', 'or', 'not', 'path']
        self.terms = self.ng.terminals

        # self.num_features = num_sensors
        self.num_actions = len(self.operators) + len(self.paths) + len(self.terms)

    def step(self, action):
        # Apply transition
        next_state, reward, done = self.apply_transition(action)

        # Translate curent tree representation to sth the agent can actually learn on
        # ...

        return next_state, reward, done, dict()


    def apply_transition(self, action):
        # Parse action
        if action < len(self.operators):  # Action is an operator
            operator = self.operators[action]
            if operator == 'and': structure = (structures.sensor.sand, 2)
            elif operator == 'or':  structure = (structures.sensor.sor, 2)
            elif operator == 'path':  structure = (structures.sensor.spath, 3)
            elif operator == 'not':   structure = (structures.sensor.snot, 1)

            # print 'pick action - op '+operator
        elif action < len(self.operators) + len(self.paths):  # Action is a path size
            action = action - len(self.operators)
            path_size = self.paths[action]
            structure = (path_size, 0)

            # print 'pick action - path '+str(path_size)
        else:  # Action is a term
            action = action - len(self.operators) - len(self.paths)
            term = self.terms[action]
            structure = (term, 0)

            # print 'pick action - term '+str(term)

        # Get place in the tree to append node
        if -1 in self.root_node.children:  # We are at the root node
            # Check if its content is an integer, then its parent has to be a path
            if not (isinstance(structure[0], int)):
                node = Node(self.root_node, structure[0], structure[1])
                self.root_node.setChild(0, node)
                # print 'ROOT OK - ' + str(self.root_node.children[0].contents)
        else: 
            self.add_node(self.root_node, structure)
            # if self.add_node(self.root_node, structure):
            #     print 'add node - True'
            # else:
            #     print 'add node - False'

        # Check if tree compiles
        done = self.verify_done(self.root_node)

        # print 'done - ' + str(done)
        # print '\n'

        # If compiles, compute reward
        if not done:
            reward = -1
        else:
            reward = self.compute_reward(self.root_node)

            # Remove this later!!!!
            print 'reward - ' + str(reward)
            print '-----------------------------------------------------\n\n\n\n'
            #time.sleep(1)
            self.reset()
            # exit(1)

        state = 'bla'

        return state, reward, done
    
    def add_node(self, parent, structure, curr_depth=1):
        for index, child in enumerate(parent.children): 
            # print 'parent children - ' + str(parent.children)
            #time.sleep(0.2)
            if child == -1: 
                if curr_depth < self.min_depth:  # Can't pick terminal nodes
                    # print 'ENTROU AQUI - min_depth CANNOT pick terminal'
                    #time.sleep(0.2)

                    if structure[1] != 0:  # Valid arity
                        node = Node(parent, structure[0], structure[1])
                        parent.setChild(index, node)
                        # print 'node - ' + str(node.contents) + '\t parent - ' + str(parent.contents)
                        # print 'added'
                        return True
                elif curr_depth >= self.max_depth:  # Has to pick a terminal
                    # print 'ENTROU AQUI - max_depth HAS TO pick terminal'
                    #time.sleep(0.2)

                    if structure[1] == 0:  # Valid arity
                        # Check if its content is an integer, then its parent has to be a path
                        if (isinstance(structure[0], int) and parent.arity == 3 and index == 2) or (not isinstance(structure[0], int) and index != 2):
                            node = Node(parent, structure[0], structure[1])
                            parent.setChild(index, node)
                            # print 'node - ' + str(node.contents) + '\t parent - ' + str(parent.contents)
                            # print 'added'
                            return True
                else: # Pick anything
                    # print 'ENTROU AQUI - pick ANYTHING'
                    #time.sleep(0.2)

                    # Check if its content is an integer, then its parent has to be a path
                    if (isinstance(structure[0], int) and parent.arity == 3 and index == 2) or (not isinstance(structure[0], int) and index != 2):
                        node = Node(parent, structure[0], structure[1])
                        parent.setChild(index, node)
                        # print 'node - ' + str(node.contents) + '\t parent - ' + str(parent.contents)
                        # print 'added'
                        return True
            else: 
                # print 'ENTROU AQUI - continue search'
                #time.sleep(0.2)
                self.add_node(child, structure, curr_depth+1)
    
    # def add_node(self, parent, structure, curr_depth=1):
    #     if len(parent.children) == 0 or -1 not in parent.children: # Can't add nodes to the parent
    #         return False
    #     else:
    #         for index, child in enumerate(parent.children): 
    #             if child == -1: 
    #                 if curr_depth < self.min_depth:  # Can't pick terminal nodes
    #                     if structure[1] != 0:  # Valid arity
    #                         if (isinstance(structure[0], int) and parent.arity == 3 and index == 2) or not isinstance(structure[0], int):
    #                             node = Node(parent, structure[0], structure[1])
    #                             parent.setChild(index, node)
    #                             # print 'node - ' + str(node.contents)
    #                             return True
    #                         else:
    #                             return False
    #                     else:
    #                         return False
    #                 elif curr_depth >= self.max_depth:  # Has to pick a terminal
    #                     if node.arity == 0:  # Valid arity
    #                         # Check if its content is an integer, then its parent has to be a path
    #                         if (isinstance(structure[0], int) and parent.arity == 3 and index == 2) or not (isinstance(structure[0], int)):
    #                             node = Node(parent, structure[0], structure[1])
    #                             parent.setChild(index, node)
    #                             # print 'node - ' + str(node.contents)
    #                             return True
    #                         else:
    #                             return False
    #                     else:
    #                         return False
    #                 else: # Pick anything
    #                     # Check if its content is an integer, then its parent has to be a path
    #                     if (isinstance(structure[0], int) and parent.arity == 3 and index == 2) or not (isinstance(structure[0], int)):
    #                         node = Node(parent, structure[0], structure[1])
    #                         parent.setChild(index, node)
    #                         # print 'node - ' + str(node.contents)
    #                         return True
    #                     else:
    #                         return False
    #             else: 
    #                 return self.add_node(child, structure, curr_depth+1)
    
    def verify_done(self, parent):
        try:
            parent.compile()
            parent.resetCompilation()
            return True
        except:
            return False
    
    def compute_reward(self, p):
        # Fitness code from Nir
        actual = self.ms.evaluate_sensor_on_traces(self.traces, p.compile())
        tp=set(self.desired[0]) & set(actual[0])
        tn=set(self.desired[1]) & set(actual[1])
        fp=set(actual[0]) & set(self.desired[1])
        fn=set(actual[1]) & set(self.desired[0])
        shouldBeFitness=(len(tp)+len(tn)-len(fp)-len(fn))
        fitness = shouldBeFitness if shouldBeFitness>0 else 0
        # print p.compile()
        return fitness

    def reset(self):
        self.curr_depth = 1
        self.root_node = Node(None, None, 1)

        # next = Node(self.root_node, structures.sensor.sand, 2)
        # self.root_node.setChild(0, next)
        # next.setChild(0, Node(next, 'bla', 0))
        # neg = Node(next, structures.sensor.snot, 1)
        # next.setChild(1, neg)
        # neg.setChild(0, Node(next, 'blaneg', 0))

        # pprint(self.root_node.compile())
        # print('\n')
        # pprint(next.compile())

        return self.root_node

    def close(self):
        self.reset()



if __name__ == "__main__":
    print("bla")
