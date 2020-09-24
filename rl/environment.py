import numpy as np


class Environment():
    
    def __init__(self, num_sensors=20, max_sensors=3, no_op=False):
        self.num_sensors = num_sensors
        self.max_sensors = max_sensors

        self.num_features = num_sensors
        self.num_actions = num_sensors

        self.no_op = no_op
        if self.no_op: self.num_actions += 1

        self.reset()


    def step(self, action):
        # Apply transition
        next_state, reward = self.apply_transition(action)

        return next_state, reward, False, dict()


    def apply_transition(self, action):
        # Check if NO OP
        if self.no_op and action == 0:  
            reward = 0
        else:
            # If bit == 1 then flip to 0
            if self.state[action] == 1: 
                self.state[action] = 0
                reward = self.compute_reward()
            # If bit == 0 then flip to 1
            else:
                # Check whether more sensors can be added
                if sum(self.state) > self.max_sensors:  
                    reward = -1
                else: 
                    self.state[action] = 1
                    reward = self.compute_reward()
        
        return self.state, reward


    def compute_reward(self):
        # recompensa = quantas violações capturadas pelo monitor
        reward = 1
        return reward


    def reset(self):
        self.state = np.zeros(self.num_sensors, dtype=int)
        return self.state


    def close(self):
        self.reset()



if __name__ == "__main__":
    from pprint import pprint
    
    env = Environment()
    env.reset()
