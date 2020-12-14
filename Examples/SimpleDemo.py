from ESSSim.Supervisor import EvoSupervisor
from ThermalSim import ThermalNode
from ThermalSim import ThermalControllerNode, LiveLogNode

"""
This demo simulates a thermal mass and a thermal PI controller.  It also creates a third node
to visualize how these systems work together.
"""

def main():
    thermal_node = ThermalNode()
    temp_sensor_node = ThermalControllerNode(1.0, 10.0)
    live_log_node = LiveLogNode()

    supervisor = EvoSupervisor()
    thermal_inputs, thermal_outputs = supervisor.add_node(thermal_node)
    controller_inputs, controller_outputs = supervisor.add_node(temp_sensor_node)
    logger_inputs, logger_outputs = supervisor.add_node(live_log_node)

    # TODO(heidt) indexing these by array is bad form, but doing dict lookups seems verbose
    # is there a middleground?
    supervisor.connect(thermal_outputs[0].temperature, controller_inputs[0].temperature)
    supervisor.connect(controller_outputs[0].power, thermal_inputs[0].power)
    supervisor.connect(controller_outputs[0].power, logger_inputs[1].power)
    supervisor.connect(thermal_outputs[0].temperature, logger_inputs[0].temperature)


    supervisor.spin(realtime=False, nonrealtime_speedup=1)


if __name__ == "__main__":
    main()