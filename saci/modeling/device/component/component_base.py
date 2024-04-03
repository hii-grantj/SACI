from typing import Tuple, List

from .cyber_abstraction_level import CyberAbstractionLevel
from ...communication.base_comm import BaseCommunication


class ComponentBase:
    """
    A ComponentBase is the base class for all components in the system. A component, at a high-level, is any device
    in the full system that can talk to at least one other device.
    """
    __state_slots__ = ()
    __slots__ = ("name", "abstraction_level")

    def __init__(self, name=None, abstraction=CyberAbstractionLevel.UNKNOWN):
        self.name = name
        self.abstraction_level = abstraction

    #
    # Simulation Useful Functions
    #

    def state_update(self, source: "ComponentBase", data: BaseCommunication) -> List["ComponentBase"]:
        """
        A State Update function describes how a component's state changes when it receives data from another component.
        Given a source component and data, the function should return a new component (of the same type as self) with
        the updated state.

        :param source:
        :param data:
        :return:
        """
        raise NotImplementedError

    def inverse_state_update(self, state: "ComponentBase") -> List[Tuple["ComponentBase", BaseCommunication]]:
        """
        An Inverse State Update function describes what possible inputs could have caused the provided state.
        The possible inputs are a list of

        :param state:
        :return:
        """
        raise NotImplementedError

    def copy(self) -> "ComponentBase":
        """
        Copy the component
        """
        new_comp = self.__class__()
        for attr in self.__slots__:
            setattr(new_comp, attr.copy() if attr else None, getattr(self, attr))

        return new_comp
