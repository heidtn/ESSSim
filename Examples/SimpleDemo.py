from ESSSim.Supervisor import EvoSupervisor
from ThermalSim import ThermalNode
from ThermalSim import ThermalControllerNode

def main():
    thermal_node = ThermalNode()
    temp_sensor_node = ThermalControllerNode()

    supervisor = EvoSupervisor()
    thermal_inputs, thermal_outputs = supervisor.add_node(thermal_node)
    controller_inputs, controller_outputs = supervisor.add_node(temp_sensor_node)

    supervisor.connect(thermal_outputs[0].temperature, controller_inputs[0].temperature)
    supervisor.connect(controller_outputs[0].power, thermal_inputs[0].power)

    supervisor.spin()

if __name__ == "__main__":
    main()