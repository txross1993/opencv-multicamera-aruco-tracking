

# Stream
from video.stream import VideoStream
from video.stream_status import StreamStatus
from util.uri_factory.stream_uri_builder import StreamUri

# Detection-Pipeline Subject + Detector
from detection_pipeline.detection_subject.aruco_tag import ArucoTag
from detection_pipeline.stream_detector.aruco_stream_detector import ArucoTagStreamDetector
from detection_pipeline.stream_detector_wrapper import StreamSubjectDetectorWrapper


# Aruco-Specific Detections - Processor + Reporter Wrappers
from detection_pipeline.processor_reporter_wrapper import ProcessorReporterWrapper
from detection_pipeline.events_processor.aruco_tag_events_processor import ArucoTagEventsProcessor
from detection_pipeline.reporter.aruco_tag_reporter import ArucoTagReporter

# Abstract maximum dictionary
from .helpers.tag_stream_max_dict import TagStreamDetectorMaxDict
from .helpers.response_enum import HeartBeatResponse
from .helpers.streamTuple import StreamTuple

# Heartbeater
from .helpers.heartbeater import Heartbeater

# utility classes
from queue import Queue
import logging
from os import environ
from util import session_request
import json

logger = logging.getLogger('root'+'.' + __name__)

class TagStreamManager(TagStreamDetectorMaxDict, Heartbeater):
    """ This implementation of AbstractMaxDict implements StreamTuple as a dictionary item
    
    Arguments:
        AbstractMaxDict {[AbstractMaxDict]} -- Abstract dictionary with a max number of items
    """
    
    def __init__(self, orchestrator_host, max_managed_streams):
        super().__init__()
        self.detector_to_processor_q = Queue()
        self._subject = ArucoTag()
        self.setMax(max_managed_streams)
        self.setupDict()
        self._orchestrator = orchestrator_host
        self._rejected_stream_endpoint = str(self._orchestrator)+'/rejected_stream'
        self._managed_stream_endpoint = str(self._orchestrator) + '/heartbeat'
        self.set_destination(self._managed_stream_endpoint)
        self._reject_streams = set()
        

    # Iinitalize subject for use by all stream-detectors #
    ######################################################
    def setupSubject(self, subjectFeaures):
        self._subject.loadFeatures(subjectFeaures)

    # Initialize the processing-reporting pipeline for all stream-detectors #
    #########################################################################
    def initializeProcessingPipeline(self):
        self.PROCESSING_PIPELINE = ProcessorReporterWrapper(processingQ=self.detector_to_processor_q,
                                                    processor=ArucoTagEventsProcessor(),
                                                    reporter=ArucoTagReporter(),
                                                    startTimeout=2)

    ## Handle adding a stream ##
    ############################
    def addStream(self, stream_id):
        logger.debug("Attempting to add stream: {}".format(stream_id))

        newStreamDetector = self.setupNewDetector(stream_id)

        if newStreamDetector is not None:
            newStreamTuple = self.setup_streamTuple(stream_id, newStreamDetector)
            if self.added_to_dict(newStreamTuple):
                self.remove_reject(stream_id)
                self.startStreamDetector(newStreamDetector)
                logger.debug("STARTED new stream-detector: {}".format(newStreamDetector))
        else:
            self.reject_stream(stream_id)

    def setup_streamTuple(self, stream_id, stream_detector):
        stream_tuple = StreamTuple(stream_id, stream_detector)
        return stream_tuple

    def added_to_dict(self, stream_tuple):
        response = self.addToDict(stream_tuple)
        return bool(response==HeartBeatResponse.ADDED)

    def setupNewDetector(self, stream_id):        
        stream_detector = self.getNewDetector()
        stream = self.getNewStream(stream_id)       
        stream.setupStream()

        if stream.status == StreamStatus.READY:
            newStreamDetector = self.getNewStreamDetector(stream_detector, stream)
            newStreamDetector.setupDetector(2)
            logger.debug("CREATED new stream-detector: {}".format(newStreamDetector))
        else:
            logger.debug("NOT READY to stream: {}. Cancelling initialization on stream".format(stream_id))
            del(stream, stream_detector)
            newStreamDetector = None

        return newStreamDetector

    def getNewStreamDetector(self, new_stream_detector, new_stream):
        return StreamSubjectDetectorWrapper(subject=self._subject,
                                            detector=new_stream_detector,
                                            stream=new_stream,
                                            eventsQueue=self.detector_to_processor_q
                                           )

    def getNewStream(self, stream_id):
        return VideoStream(stream_id)

    def getNewDetector(self):
        return ArucoTagStreamDetector()

    def startStreamDetector(self, stream_detector):
        if self.PROCESSING_PIPELINE._stopped==True:
            self.PROCESSING_PIPELINE.start()

        stream_detector.startThreads()

    ## Handle rejected streams ##
    #############################

    
    def reject_stream(self, stream_id):
        
        self._reject_streams.add(stream_id)
        self.send_rejected_stream_response(stream_id)

    def rejected_stream_payload(self, stream_id):
        return json.dumps({'pod_name': environ['HOSTNAME'], 'stream': stream_id })

    def send_rejected_stream_response(self, stream_id):
        try:
            response = session_request.requests_retry_session() \
                        .post(self._rejected_stream_endpoint, timeout=2, data=self.rejected_stream_payload(stream_id))    
        except Exception as x:
            logger.warning("Orchestrator unreachable: {}".format(x.__class__.__name__))

    def is_reject(self, stream_id) -> bool:
        return bool(stream_id in self._reject_streams)

    def remove_reject(self, stream_id):
        if self.is_reject(stream_id):
            self._reject_streams.remove(stream_id)

    ## Handle removing a stream ##
    ##############################

    def removeStream(self, stream_id):
        logger.debug("Attempting to remove stream: {}".format(stream_id))
        if any(self._managed_items_dict.values()):
            for streamTuple in self._managed_items_dict.values():
                if streamTuple.stream_id==stream_id:
                    self.stopStreamDetector(streamTuple)
                    self.removeFromDict(streamTuple)    

    def stopStreamDetector(self, streamTuple):
        streamTuple.stream_detector.stopThreads(0.5)

    
    ## Heartbeater ##
    #################

    def handleHeartbeatResponse(self, response):
        # First, update stream metrics, which will update the list of managed streams in case 
        # a heartbeat has stopped responding:
        if response:
            self.getStreamMetrics()
            
            currentlyManaged = set(self.getCurrentManagedStreamIdsAsList())
            logger.info("Currently Managed Streams: {}".format(currentlyManaged))

            directedToManage = set(next(iter(response.values())))
            logger.debug("Response object of to-manage streams: {}".format(directedToManage))

            streamsToAdd = directedToManage-currentlyManaged
            logger.debug("Streams to Add: {}".format(streamsToAdd))

            streamsToRemove =  currentlyManaged-directedToManage
            logger.debug("Streams to Remove: {}".format(streamsToRemove))

            for stream_id in streamsToRemove:
                self.removeStream(stream_id)

            for stream_id in streamsToAdd:
                self.addStream(stream_id)

            self.setPayload(self.getStreamMetricPayload())
            #logger.info("Set heartbeat payload {}".format(self.payload))

    def getCurrentManagedStreamIdsAsList(self):
        currentlyManagedStreams = []
        if any(self._managed_items_dict.values()):
            currentlyManagedStreams = [streamTuple.stream_id for streamTuple in self._managed_items_dict.values() if streamTuple is not None]
        
        return currentlyManagedStreams

    def getStreamMetrics(self):
        if any(self._managed_items_dict.values()):
            for streamTuple in self._managed_items_dict.values():
                if streamTuple is not None:
                    if not any(streamTuple.stream_detector.streamMetrics):
                        self.removeStream(streamTuple.stream_id)

    def getStreamMetricPayload(self):
        numStreamSlots = len(self._managed_items_dict)
        if any(self._managed_items_dict.values()):
            arrayOfStreamIds = [streamTuple.stream_id for streamTuple in self._managed_items_dict.values() if streamTuple is not None] 
        else:
            arrayOfStreamIds = []
        return json.dumps({ 'num_streams': numStreamSlots, 
                 'streams': arrayOfStreamIds, 
                 'pod_name': environ['HOSTNAME'] })
    