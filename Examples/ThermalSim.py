from ESSSim.Node import StateSpaceNode, TimeDomainNode
from ESSSim.InputOutput import InputOutput, InputOutputGroup
import numpy as np
import clive_log

temperature_group = {"temperature": InputOutput(float, 0)}
power_group = {"power": InputOutput(float, 0)}

class ThermalNode(StateSpaceNode):
    """
    This simulates a conduction thermal mass only with a heater input
    """
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
        self.output.temperature.value = self.state[0]

    def get_state(self):
        return self.state

    def get_state_derivative(self):
        # very very simple conduction only thermal model (Ta - Ts)*UA + Pin where UA is just 1
        # assuming the environmental boundary conditions are just 25C and Pin is the power of the
        # heater in watts
        mCp = 10.0*0.466 # a steel block of 10kg with a surface area of 1m^2
        deriv = (25 - self.state[0]) * 5 / mCp + self.input.power.value/mCp
        #print("deriv is: ", deriv)
        return np.array([deriv])


class ThermalControllerNode(TimeDomainNode):
    """
    This is a simple PI controller that attempts to get the temperature to 50C.  Its
    tuned improperly on purpose to show the overshoot of the controller.
    """
    def __init__(self, Kp, Ki):
        self.input = InputOutputGroup(temperature_group)
        self.output = InputOutputGroup(power_group)
        self.state = 0.0
        self.I = 0.0
        self.Kp = Kp
        self.Ki = Ki
        self.last_time = None
        
    def get_inputs(self):
        return [self.input]

    def get_outputs(self):
        return [self.output]

    def update(self, current_time):
        if self.last_time == None:
            self.last_time = current_time
            return 0.0
        else:
            dt = current_time - self.last_time
            error = 50 - self.input.temperature.value
            self.I += error*dt
            self.output.power.value = max(error*self.Kp + self.Ki*self.I, 0.0)
            self.last_time = current_time


class LiveLogNode(TimeDomainNode):
    def __init__(self):
        self.input = [InputOutputGroup(temperature_group), InputOutputGroup(power_group)]
        self.output = None
        self.logger = clive_log.Context("temperatures")
        self.logger.add_graph_field("temperature")
        self.logger.add_text_field("power")
        self.temperatures = [0]
        self.last_time = None
    
    def get_inputs(self):
        return self.input

    def get_outputs(self):
        return [self.output]

    def update(self, current_time):
        if not self.last_time or (current_time - self.last_time > 0.1):
            self.temperatures.append(self.input[0].temperature.value)
            if(len(self.temperatures) > 50):
                self.temperatures.pop(0)
            self.last_time = current_time
            self.logger.write_text_field("power", self.input[0].temperature.value)
            self.logger.update_graph_field("temperature", self.temperatures)
            self.logger.display()