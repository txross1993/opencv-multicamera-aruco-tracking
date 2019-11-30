from events_processor.abstract_events_processor import AbstractEventsProcessor
from event_struct.abstract_event_struct import AbstractEventStruct
from event_struct.location_point import Point
from .helpers.aruco_tag_comparer import TagComparer
from .helpers.aruco_tag_states import TagComparisonStates
from expiringdict import ExpiringDict
import logging
from util.timing import timing
from os import environ

logger = logging.getLogger('root'+'.' + __name__)

class ArucoTagEventsProcessor(AbstractEventsProcessor):
    try:
        cache = ExpiringDict(max_len=int(environ['DICT_MAXLENGTH']), max_age_seconds=int(environ['DICT_MAXAGE']))
    except KeyError:
        cache = ExpiringDict(3000, 120)

    def __init__(self):
        super().__init__()

    def addToCache(self, event):
        entry = { event.tagId: event }
        ArucoTagEventsProcessor.cache.update(entry)
        logger.debug("Adding detection event to cache: {}".format(event.tagId))

    def checkIfInCache(self, event):
        try:
            ArucoTagEventsProcessor.cache[event.tagId]
            logger.debug("Tag Id {} exists in Aruco Tag Cache".format(event.tagId))
            return True
        except KeyError:
            return False
            logger.debug("Tag Id {} does NOT exist in Aruco Tag Cache".format(event.tagId))

    def acceptEvent(self, event):
        self.putOutputQ(event)
        logger.info('PROCESSOR - PROCESSED EVENT - for tag {}'.format(event.tagId))

    # @staticmethod
    # def get_tag_stream_key(event):
    #     key = str(event.tagId)+'-'+str(event.sourceStream)
    #     return key

    # def handleNewStream(self, event):
    #     key = ArucoTagEventsProcessor.get_tag_stream_key(event)
    #     tagState = None
    #     try:
    #         ArucoTagEventsProcessor.tag_stream_cache[key]
    #         ''' Key exists, return tag state of UNCHANGED '''
    #         tagState = TagComparisonStates.UNCHANGED
    #     except KeyError:
    #         ArucoTagEventsProcessor.tag_stream_cache[key]=event
    #         ''' Key didn't exist, return tag state of UPDATED '''
    #         tagState = TagComparisonStates.UPDATED
    #     logger.info('PROCESSOR - NEWSTREAM EVENT: {}, STATE: {}'.format(event.toDict(), tagState))
    #     return tagState
        
    @timing
    def processEvent(self, event):
        # logger.debug("PROCESSING EVENTS - events in process for {}".format(self.__class__.__name__))
        
        #logger.info("Tag {} seen by stream_id {} at {}".format(event.tagId, event.sourceStream, (event.location.x, event.location.y)))
        self.acceptEvent(event)

        # tagId = event.tagId
        # if self.checkIfInCache(event):
        #     try:
        #         tagState = TagComparer(event, ArucoTagEventsProcessor.cache[tagId]).compare()
        #     except KeyError:
        #         ''' The comparison started just as cache expired '''
        #         tagState = TagComparisonStates.NEW

        #     # if tagState == TagComparisonStates.NEWSTREAM:
        #     #     tagState = self.handleNewStream(event)
        #     if tagState != TagComparisonStates.UNCHANGED:
        #         logger.info("TAG STATE {}".format(tagState))

        #     if tagState == TagComparisonStates.ERR:
        #         logger.warning( """Possible homography error for stream {}.
        #         First event: {}
        #         Second event with homography error: {}""".format(event.sourceStream, ArucoTagEventsProcessor.cache[event.tagId].toDict(), event.toDict()))
        #     # elif tagState == TagComparisonStates.UNCHANGED:
        #     #     pass           
        #     elif tagState == TagComparisonStates.UPDATED or tagState == TagComparisonStates.NEW:
        #         self.acceptEvent(event)
        #         self.addToCache(event)
        # else:
        #     logger.info("TAG {} NOT IN CACHE - NEW TAG".format(event.tagId))
        #     ''' If tag isn't in the cache, then it's a new event, so publish it '''
        #     self.acceptEvent(event)
        #     self.addToCache(event)
        