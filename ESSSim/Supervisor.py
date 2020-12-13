import time
from collections import namedtuple

"""
TODO:
 - verify that all inputs are connected
 - verify that only outputs are connected to inputs
 - verify node input/out types match
 - verify each input is connected to only one output
"""

Connection = namedtuple('Connection', ['input', 'output'])

class EvoSupervisor:
    def __init__(self):
        self.nodes = []
        self.inputs = []
        self.outputs = []
        self.connections = []
        self.last_time = time.time()
    
    def add_node(self, node):
        self.nodes.append(node)
        for input in node.get_inputs():
            self.inputs.append(input)

        for output in node.get_outputs():
            self.outputs.append(node.get_outputs())

        return node.get_inputs(), node.get_outputs()

    def connect(self, input, output):
        #  TODO verify these are correct types
        self.connections.append(Connection(input, output))
        
    def spin(self, realtime=True, nonrealtime_step=0.1, nonrealtime_speedup=20):
        #  TODO check all node inputs are connected
        #  TODO check each input only has one output (outputs can go to multiple inputs though
        #  TODO iterate through each connection, pass each output to each associated input
        #  then perform one increment
        if not realtime:
            curtime = 0
            self.last_time = 0
        while True:
            if realtime:
                curtime = time.time()
            else:
                curtime += nonrealtime_step
            dt = curtime - self.last_time
            for node in self.nodes:
                if node.node_type == "state_space":
                    # Forward Euler step
                    node.set_state(node.get_state() + node.get_state_derivative()*dt)
                elif node.node_type == "time_domain":
                    node.update(curtime)

            # After we've done one forward step, update all of the inputs to match the new outputs
            for connection in self.connections:
                connection.input.value = connection.output.value

            if realtime:
                self.last_time = time.time()
            else:
                self.last_time = curtime
                time.sleep(nonrealtime_step/nonrealtime_speedup)