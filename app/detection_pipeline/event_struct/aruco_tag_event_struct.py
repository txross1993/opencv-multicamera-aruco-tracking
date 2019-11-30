from .abstract_event_struct import AbstractEventStruct
from .location_point import Point

class TagEventStruct(AbstractEventStruct):

    def __init__(self):
        super().__init__()
        self._tagId = int()
        self._location = None
        self._srcStream = str()
        self._ts = float()
        
 
    def __eq__(self, other):
        return self._tagId==other.tagId

    def toDict(self):
        return { 'tagId': self._tagId, 'location': self._location.__dict__, 'sourceStream': self._srcStream, 'timestamp': self._ts}

    @property
    def tagId(self):
        return self._tagId

    def setTagId(self, tagId):
        self._tagId = tagId

    @property
    def timestamp(self):
        return self._ts

    def setTimestamp(self, ts):
        self._ts = ts

    @property
    def location(self):
        return self._location

    def setLocation(self, point:Point):
        self._location = point

    @property
    def sourceStream(self):
        return self._srcStream

    def setSourceStream(self, sourceStream):
        self._srcStream = sourceStream