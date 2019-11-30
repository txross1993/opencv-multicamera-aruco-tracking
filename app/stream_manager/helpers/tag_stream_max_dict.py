from generic_base_classes.abstract_max_dict import AbstractMaxDict
from .streamTuple import StreamTuple
from .response_enum import HeartBeatResponse
import logging

logger = logging.getLogger('root'+'.' + __name__)

class TagStreamDetectorMaxDict(AbstractMaxDict):

    def __init__(self):
        super().__init__()

    def addToDict(self, streamTuple:StreamTuple):
        if streamTuple is None:
            return
            
        if self.isDuplicateValue(streamTuple):
            response = HeartBeatResponse.DUPLICATE
        else:
            try:
                nextEmptyKey = self.getNextEmptyKey()
                self._managed_items_dict.update({nextEmptyKey:streamTuple})
                response = HeartBeatResponse.ADDED
            except:
                response = HeartBeatResponse.FULL
        return response

    def isDuplicateValue(self, streamTuple:StreamTuple):
        logger.debug("Checking for duplicate value")
        duplicateCheck = False
        if any(self._managed_items_dict.values()):
            duplicateCheck = any([streamTuple.__eq__(dictTuple) for dictTuple in self.filterOutNoneValues()])
        return duplicateCheck

    def filterOutNoneValues(self):
        ''' Return only values in self._managed_items_dict that are not NONE '''
        return [v for v in self._managed_items_dict.values() if v is not None]


    def removeFromDict(self, streamTuple:StreamTuple):
        for streamKey,streamTupValue in self._managed_items_dict.items():
            if streamTuple.__eq__(streamTupValue):
                self._managed_items_dict.update({streamKey: None})
                logger.debug("Removed stream: {}".format(streamTupValue.stream_id))

    def doesStreamIdExist(self, stream_id):
        return any([stream_id==streamTuple.stream_id for streamTuple in self._managed_items_dict.values()])
