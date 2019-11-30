from enum import Enum

class TagComparisonStates(Enum):
    NEW = 1
    UNCHANGED = 2
    UPDATED = 3
    ERR = 4
    NEWSTREAM = 5