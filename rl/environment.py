import numpy as np
from copy import copy, deepcopy
from node import Node
from structures.sensor import * 
import os
import pickle

class Environment():
    
    def __init__(self, domain_name, instance, tag, ng, modelSensor, traces, ms):
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

        # Q-net stuff
        self.num_actions = (len(self.operators) + len(self.paths) + len(self.terms)) + 1
        self.num_features = ((self.num_actions-1)/2) + 1

        # Episode control
        self.max_steps = 20

        # History
        self.history = []
        self.history_filename = 'rl/output/' + str(domain_name) + '-' + str(tag) + '{0}'.format("%02d" % instance) + '-history.pkl'
        if not os.path.exists('rl/output/'):
            os.makedirs('rl/output')


    def step(self, action):
        # Apply transition
        next_state, reward, done = self.apply_transition(action)

        # Increment step
        self.curr_step += 1

        return next_state, reward, done, dict()


    def apply_transition(self, action):
        # Check if action is to do nothing
        if action == self.num_actions-1:
            done = self.verify_done(self.root_node)
            reward = 0
            return self.state, reward, done
        
        # Check if action is to add or remove a node
        if action > (self.num_actions-1)/2:  # Remove node
            self.action = action/2
            action = action/2
            self.add = False
        else:  # Add node
            self.action = action
            self.add = True

        # Parse action
        if self.action < len(self.operators):  # Action is an operator
            operator = self.operators[action]
            if operator == 'and': structure = (structures.sensor.sand, 2)
            elif operator == 'or':  structure = (structures.sensor.sor, 2)
            elif operator == 'path':  structure = (structures.sensor.spath, 3)
            elif operator == 'not':   structure = (structures.sensor.snot, 1)
        elif self.action < len(self.operators) + len(self.paths):  # Action is a path size
            action = action - len(self.operators)
            path_size = self.paths[action]
            structure = (path_size, 0)
        else:  # Action is a term
            action = action - len(self.operators) - len(self.paths)
            term = self.terms[action]
            structure = (term, 0)

        # Add or remove a valid node
        if self.add == True:  # Add node
            # Get place in the tree to append node
            if -1 in self.root_node.children:  # We are at the root node
                # Check if its content is an integer, then its parent has to be a path
                if not (isinstance(structure[0], int)):
                    node = Node(self.root_node, structure[0], structure[1])
                    self.root_node.setChild(0, node)
                    # Change state
                    self.timestep += 1
                    self.state[self.action] += 1
                    self.state[-1] = self.timestep
            else:  # Add somewhere valid in the tree
                self.add_node(self.root_node, structure)
        else:  # Remove node
            self.remove_node(self.root_node, structure)

        # Check if tree compiles
        done = self.verify_done(self.root_node)

        # If compiles, compute reward
        if not done:
            reward = -1
        else:
            reward = self.compute_reward(self.root_node)

        return self.state, reward, done
    

    def add_node(self, parent, structure, curr_depth=1):
        for index, child in enumerate(parent.children): 
            if child == -1: 
                if curr_depth < self.min_depth:  # Can't pick terminal nodes
                    if structure[1] != 0:  # Valid arity
                        # Add node
                        node = Node(parent, structure[0], structure[1])
                        parent.setChild(index, node)
                        # Change state
                        self.timestep += 1
                        self.state[self.action] += 1
                        self.state[-1] = self.timestep
                        return True
                elif curr_depth >= self.max_depth:  # Has to pick a terminal
                    if structure[1] == 0:  # Valid arity
                        # Check if its content is an integer, then its parent has to be a path
                        if (isinstance(structure[0], int) and parent.arity == 3 and index == 2) or (not isinstance(structure[0], int) and index != 2):
                            node = Node(parent, structure[0], structure[1])
                            parent.setChild(index, node)
                            # Change state
                            self.timestep += 1
                            self.state[self.action] += 1
                            self.state[-1] = self.timestep
                            return True
                else: # Pick anything
                    # Check if its content is an integer, then its parent has to be a path
                    if (isinstance(structure[0], int) and parent.arity == 3 and index == 2) or (not isinstance(structure[0], int) and index != 2):
                        node = Node(parent, structure[0], structure[1])
                        parent.setChild(index, node)
                        # Change state
                        self.timestep += 1
                        self.state[self.action] += 1
                        self.state[-1] = self.timestep
                        return True
            else: 
                self.add_node(child, structure, curr_depth+1)


    def remove_node(self, parent, structure, curr_depth=1):
        for index, child in enumerate(parent.children): 
            if child != -1: 
                if child.contents == structure[0] and child.arity == structure[1]: 
                    # Remove node
                    child = -1
                    # Change state
                    self.timestep += 1
                    self.state[self.action] -= 1
                    self.state[-1] = self.timestep
                    return True
                else: 
                    self.remove_node(child, structure, curr_depth+1)
    

    def verify_depth(self, parent, curr_depth=1):
        if curr_depth == self.min_depth: return True
        for index, child in enumerate(parent.children):
            if child != -1: return self.verify_depth(child, curr_depth+1)
            else: return False


    def verify_done(self, parent):
        if self.curr_step >= self.max_steps:
            if self.verify_depth(parent):
                try:
                    parent.compile()
                    parent.resetCompilation()
                    return True
                except:
                    return False
            else:
                return False
        else:
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

        # Save to history
        self.history.append((fitness, p.compile()))

        # Write current history to file
        #print 'Writing history to file...'
        with open(self.history_filename, 'w+') as f:
            pickle.dump(self.history, f)

        self.last_state = p

        return fitness


    def get_last_state(self):
        return self.last_state


    def reset(self):
        self.curr_depth = 1
        self.root_node = Node(None, None, 1)
        self.timestep = 0
        self.state = np.zeros(self.num_features, dtype=int)
        # Current episode step
        self.curr_step = 0

        return self.state


    def close(self):
        self.reset()



if __name__ == "__main__":
    pass
