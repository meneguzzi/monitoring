import numpy as np
from copy import copy
from node import Node
from structures.sensor import * 
from pprint import pprint
import random

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
        self.nodes = list()
        self.curr_depth = 0

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
        elif action < len(self.operators) + len(self.paths):  # Action is a path size
            action = action - len(self.operators)
            path_size = self.paths[action]
            structure = (path_size, 0)
        else:  # Action is a term
            action = action - len(self.operators) - len(self.paths)
            term = self.terms[action]
            structure = (term, 0)

        # Get place in the tree to append node
        if len(self.nodes) == 1:  # We are at the root node
            node = Node(self.root_node, structure[0], structure[1])
            self.root_node.setChild(0, node)
            self.nodes.append(node)
        else: 
            # Get parent node and child
            parent = self.get_node(self.root_node)
            if parent == False:
                print 'WHAAAAAAAAAAAAAAAAT'
                exit(1)
            
            for index, child in enumerate(parent.children):
                if child == -1: break
                else: continue

            # Add node
            if self.curr_depth < self.min_depth:  # Can't pick terminal nodes
                if structure[1] != 0:  # Valid arity
                    node = self.add_node(self.root_node, structure)
                    self.nodes.append(node)
                    self.curr_depth += 1
            if self.curr_depth >= self.max_depth:  # Has to pick a terminal
                if node.arity == 0:  # Valid arity
                    node = self.add_node(self.root_node, structure)
                    self.nodes.append(node)
                    self.curr_depth += 1

        # Check if tree compiles
        done = self.verify_done(self.root_node)

        # if len(self.nodes) == 3:
        #     print self.root_node.compile()

        # If compiles, compute reward
        if not done:
            reward = -1
        else:
            reward = self.compute_reward(self.root_node)
            print reward
            print '!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n'
            self.reset()

        state = 'bla'
        # print action, '\t', reward, '\t', len(self.nodes)

        return state, reward, done
    
    def get_node(self, parent):
        for index, child in enumerate(parent.children):
            if child == -1 and index <= parent.arity: 
                return parent
            return self.get_node(child)
    
    def add_node(self, parent, structure):
        for index, child in enumerate(parent.children):
            if child == -1 and index <= parent.arity: 
                node = Node(parent, structure[0], structure[1])
                parent.setChild(index, node)
                return node
            return self.add_node(child, structure)
    
    def verify_done(self, parent):
        for index, child in enumerate(parent.children):
            if child == -1 and index <= parent.arity: 
                return False
            elif index+1 == parent.arity:
                return True
            return self.verify_done(child)

    def compute_reward(self, p):
        # Fitness code from Nir
        actual = self.ms.evaluate_sensor_on_traces(self.traces, p.compile())
        tp=set(self.desired[0]) & set(actual[0])
        tn=set(self.desired[1]) & set(actual[1])
        fp=set(actual[0]) & set(self.desired[1])
        fn=set(actual[1]) & set(self.desired[0])
        shouldBeFitness=(len(tp)+len(tn)-len(fp)-len(fn))
        fitness = shouldBeFitness if shouldBeFitness>0 else 0
        print p.compile()
        return fitness


    def reset(self):
        self.curr_depth = 1
        self.root_node = Node(None, None, self.curr_depth)
        self.nodes = [self.root_node]

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
