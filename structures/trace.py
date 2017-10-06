from state import State
from sensor import Sensor


class Trace():
    """ A trace from a plan, this should consist of a sequence of states"""

    def __init__(self, trace):
        self.trace = trace

    def __setitem__(self, key, value):
        if isinstance(value, State):
            self.trace[key] = value
        else:
            raise ValueError('Value is not a state.')

    def __getitem__(self, item):
        return self.trace

    def models(self, sensor, state, domain):
        assert isinstance(sensor, Sensor)
        assert isinstance(state, State)
        return sensor.is_model_of(self, state, domain)
