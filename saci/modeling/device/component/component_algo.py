from typing import List, Dict

from .component_base import ComponentBase
from .cyber_abstraction_level import CyberAbstractionLevel

# TODO: maybe dont bind to z3
import claripy


class ComponentAlgorithmic(ComponentBase):
    __state_slots__ = ComponentBase.__state_slots__ + ("conditions",)
    __slots__ = ComponentBase.__slots__ + ("conditions", "variables",)

    def __init__(
        self,
        abstraction=CyberAbstractionLevel.ALGORITHMIC,
        variables: Dict[str, claripy.ast.bv.BV] = None,
        conditions: List[claripy.ast.bool.Bool] = None,
        **kwargs
    ):
        super().__init__(abstraction=abstraction, **kwargs)
        self.variables = variables or {}

        self.conditions = conditions or []

    @property
    def v(self):
        return self.variables
