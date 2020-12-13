from abc import ABC, abstractmethod
from ESSSim.InputOutput import InputOutputGroup
from typing import List

class Node(ABC):
    @abstractmethod
    def get_inputs(self) -> List[InputOutputGroup]:
        pass

    @abstractmethod
    def get_outputs(self) -> List[InputOutputGroup]:
        pass


class StateSpaceNode(Node):
    node_type = 'state_space'

    @abstractmethod
    def set_state(self, state):
        pass

    @abstractmethod
    def get_state(self):
        pass

    @abstractmethod
    def get_state_derivative(self):
        pass

class TimeDomainNode(Node):
    node_type = "time_domain"

    @abstractmethod
    def update(self, time):
        pass