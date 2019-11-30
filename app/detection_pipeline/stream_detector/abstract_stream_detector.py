from abc import ABCMeta, abstractmethod
from threading import Thread, Event
from queue import Queue
import logging
from video.stream import VideoStream
from video.frame import Frame, NullFrame
from util import timestamper
from detection_pipeline.detection_subject.abstract_detection_subject import AbstractDetectionSubject
from detection_pipeline.detection_subject.null_subject import NullSubject
from events_processor.abstract_events_processor import AbstractEventsProcessor
from event_struct.abstract_event_struct import AbstractEventStruct
from time import sleep
from util.counts_per_sec import CountsPerSec as CPS

logger = logging.getLogger('root'+'.' + __name__)

class AbstractStreamDetector(metaclass=ABCMeta):
    """ The function of a detector is to accept a frame to detect features of a subject 
    and output raw data points representing the detections of the subject in the frame. 
    The raw data points will be sent to the event construct.
    
    Keyword Arguments:
        metaclass ABCMeta
    
    Returns:
        Raw detection data (regarding pixels) and timestamp of detection
    """
    
    def __init__(self):
        super().__init__()
        self._subject = NullSubject()
        self._stream = None
        self._outputQ = None
        self._detectorThread = None
        self._stopped = False    
        self._framesRead=0        

    # Set the stream
    @property
    def stream(self):
        return self._stream

    def setStream(self, stream:VideoStream):
        self._stream = stream

    # Set the output queue
    @property
    def outputQ(self):
        return self._outputQ

    def setOutputQ(self, queue:Queue):
        self._outputQ = queue
        logger.debug("{}'s output queue has been set".format(self.__class__.__name__))

    @property
    def streamDetectorThread(self):
        return self._detectorThread

    def setStreamDetectorThread(self, timeout):
        self._detectorThread = Thread(name=self._stream.name, target=self.processStream, args=(timeout,))
        logger.debug("{}'s detector thread has been instantiated with stream {}".format(self.__class__.__name__, self._stream.name))

    # Set the subject
    @property
    def subject(self):
        return self._subject

    def setSubject(self, subject:AbstractDetectionSubject):
        self._subject = subject
        self.verifySubjectType()

    @abstractmethod
    def verifySubjectType(self):
        """Implement"""

    
    # Thread worker
    def start(self):
        if self._outputQ:
            try:
                self._stream.start()
                self._detectorThread.start()
                logger.debug("STARTED - Detector thread started for {}".format(self.__class__.__name__))
            except RuntimeError:
                logger.warning("Stream {} or Detector {} threads already running".format(self._stream.name, self))
        else:
            logger.error('Output queue for detected events has not been set!')

    def stop(self, timeout):
        self._stream.stop()
        self._stopped = True
        self._detectorThread.join(timeout)
        logger.debug("STOPPED - detector thread for stream {}".format(self._stream.name))
        return self._detectorThread.is_alive()

    def processStream(self, t):
        logger.debug("ENTERING - Entering detection thread loop for stream {}".format(self._stream.name))

        cps = CPS().start()
        while not self._stopped:
            #logger.info("STILL RUNNING - Stream-Detector still running for stream {}. Frames read so far: {}".format(self._stream.name, self._framesRead))
            # if self._outputQ.qsize() > 0:
            #         self.stream.set_read_sleep(self.stream.read_sleep+1)
            # else:
            #     if self.stream.read_sleep != 1:
            #         self.stream.set_read_sleep(1)
                        
            frame = self._stream.read()
            if type(frame) == Frame:
                self._framesRead+=1
                events = self.get_events(frame)
                self._outputQ.put(events)
                logger.info("PUT events on the detector-to-processor queue from stream {}".format(self._stream.name))
            else:
                continue
            logger.info("Loop iterations/sec: {:.0f}".format(cps.countsPerSec()))
            cps.increment()

    # Detect the subject    

    @abstractmethod
    def get_events(self, frame:Frame) -> list:
        """ Implement """

    @abstractmethod
    def composeEventStruct(self):
        """ Implement """