from typing import Tuple, List

from saci.modeling.device.component.cyber.cyber_abstraction_level import CyberAbstractionLevel
from saci.modeling.device.component.component_base import ComponentBase
from saci.modeling.device.component.component_type import ComponentType
from saci.modeling.communication.base_comm import BaseCommunication


class CyberComponentBase(ComponentBase):
    """
    A CyberComponentBase is the base class for all components in the system. A component, at a high-level, is any device
    in the full system that can talk to at least one other device.
    """
    __state_slots__ = ComponentBase.__state_slots__ + ()
    __slots__ = ComponentBase.__slots__ + ("abstraction_level",)

    def __init__(self, name=None, _type=ComponentType.CYBER, abstraction=CyberAbstractionLevel.UNKNOWN, parameters=None, ports=None):
        super().__init__(name=name, _type=_type, parameters=parameters, ports=ports)
        self.abstraction_level = abstraction
