from ..component import CyberComponentHigh, CyberComponentAlgorithmic, CyberComponentBase, CyberAbstractionLevel

from claripy import BVS


class ServoHigh(CyberComponentHigh):
    __slots__ = CyberComponentHigh.__slots__

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class ServoAlgorithmic(CyberComponentAlgorithmic):
    __slots__ = CyberComponentAlgorithmic.__slots__

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.variables["angle"] = BVS("angle", 64)

class Servo(CyberComponentBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ABSTRACTIONS = {
            CyberAbstractionLevel.HIGH: ServoHigh(),
            CyberAbstractionLevel.ALGORITHMIC: ServoAlgorithmic(),
        }
