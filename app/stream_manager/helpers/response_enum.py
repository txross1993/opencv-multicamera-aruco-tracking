from enum import Enum

class HeartBeatResponse(Enum):
    ADDED = 1
    DUPLICATE = 2
    FULL = 3