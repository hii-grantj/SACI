from typing import List

from ..device import ComponentBase


class GlobalState:
    def __init__(self, components: List[ComponentBase]):
        self.components = components
