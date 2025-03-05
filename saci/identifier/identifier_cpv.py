from dataclasses import dataclass
from typing import TypeVar

from saci.modeling import Device, CPV, ComponentBase
from saci.modeling.device.device import IdentifiedComponent, ComponentID
from saci.modeling.state import GlobalState



def get_next_components(component_id: ComponentID, device: Device) -> list[ComponentID]:
    return list(device.component_graph.successors(component_id))

class IdentifierCPV:
    def __init__(self, device: Device, initial_state: GlobalState):
        self.device = device
        self.initial_state = initial_state

    def identify(self, cpv: CPV) -> list[list[IdentifiedComponent]]:
        # Get the starting locations (components with external input)
        starting_locations: list[ComponentID] = [
            c for c, is_entry in self.device.component_graph.nodes(data="is_entry", default=False) # type: ignore
            if is_entry
        ]

        cpv_paths: list[list[ComponentID]] = []

        # CPV Path identification
        for start in starting_locations:
            stack = [(start, [start])]  # Stack stores (current_component, current_path)

            while stack:
                vertex, path = stack.pop()

                # Get the correct neighbors using the fixed function
                neighbors = get_next_components(vertex, self.device)

                for neighbor in neighbors:
                    if neighbor not in path:  # Avoid cycles in the current path
                        new_path = path + [neighbor]
                        stack.append((neighbor, new_path))

                # If the current path is valid, add it to the result
                if cpv.is_possible_path([self.device.components[comp_id] for comp_id in path]):
                    cpv_paths.append(path)

        return [[IdentifiedComponent.from_id(self.device, comp_id) for comp_id in path] for path in cpv_paths]
