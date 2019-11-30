from .aruco_tag_states import TagComparisonStates
import logging
from os import environ

logger = logging.getLogger('root'+'.' + __name__)

class TagComparer:
    try:
        timestamp_delta_threshold = int(environ['TS_THRESHOLD'])
    except Exception:
        timestamp_delta_threshold = 3000
    
    logger.debug("Timestamp delta threshold set: {}".format(timestamp_delta_threshold))

    def __init__(self, event1, event2):
        self._event1 = event1
        self._event2 = event2

        self.newLocation = self.isNewLocation()
        self.newTimestamp = self.isNewTimestamp()
        self.newStream = self.isNewStream()

    def isNewTimestamp(self):
        return abs(self._event1.timestamp - self._event2.timestamp) >= TagComparer.timestamp_delta_threshold

    def isNewLocation(self):
        newLocation =self._event1.location.__cmp__(self._event2.location)
        return newLocation

    def isNewStream(self):
        return self._event1.sourceStream!=self._event2.sourceStream

    def compare(self):
        state = None
        
        if self.newStream and not self.newTimestamp and self.newLocation:            
            state = TagComparisonStates.ERR
        elif self.newLocation:
            state = TagComparisonStates.UPDATED
        else:
            state = TagComparisonStates.UNCHANGED
        return state