from enum import Enum

class StreamStatus(Enum):
    RUNNING = 1
    STOPPED = 2
    REJECTED = 3
    READY = 4