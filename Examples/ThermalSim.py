from ESSSim.Node import StateSpaceNode, TimeDomainNode
from ESSSim.InputOutput import InputOutput, InputOutputGroup
import numpy as np
import clive_log

temperature_group = {"temperature": InputOutput(float, 0)}
power_group = {"power": InputOutput(float, 0)}

class ThermalNode(StateSpaceNode):
    def __init__(self):
        self.input = InputOutputGroup(power_group)
        self.output = InputOutputGroup(temperature_group)
        self.state = np.array([25])

    def get_inputs(self):
        return [self.input]

    def get_outputs(self):
        return [self.output]

    def set_state(self, state):
        self.state = state

    def get_state(self):
        return self.state

    def get_state_derivative(self):
        return np.array([self.state[0] - 25 + self.input.power.value])


class ThermalControllerNode(TimeDomainNode):
    def __init__(self):
        self.input = InputOutputGroup(temperature_group)
        self.output = InputOutputGroup(power_group)
        self.state = 0.0
        self.I = 0.0
        self.last_time = None
        
    def get_inputs(self):
        return [self.input]

    def get_outputs(self):
        return [self.output]

    def update(self, time):
        if self.last_time == None:
            self.last_time = time
            return 0.0
        else:
            dt = time - self.last_time
            error = 100 - self.input.temperature.value
            self.I += error*dt
            self.output.power.value = error*1.0 + self.I*0.1
            self.last_time = time
