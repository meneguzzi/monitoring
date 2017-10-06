
from action import Action


class Domain():

    def __init__(self,actions):
        self.actions = dict
        for action in actions:
            self.actions[action.name] = action

    def __getitem__(self, item):
        return self.actions[item]

    def __setitem__(self, key, value):
        self.actions[key] = value