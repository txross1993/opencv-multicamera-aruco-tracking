from .detection_subject.abstract_detection_subject import AbstractDetectionSubject
from .stream_detector.abstract_stream_detector import AbstractStreamDetector
from video.stream import VideoStream
from time import sleep
from queue import Queue
import logging

logger = logging.getLogger('root'+'.' + __name__)

class StreamSubjectDetectorWrapper:

    def __init__(self, subject:AbstractDetectionSubject, 
                       detector:AbstractStreamDetector,
                       stream:VideoStream,
                       eventsQueue:Queue):

        self._subject = subject
        self._detector = detector
        self._stream = stream
        self._eventsQ = eventsQueue

    @property
    def streamName(self):
        return self._stream.name

    @property
    def streamMetrics(self):
        return self._stream._metrics

    def setupDetector(self, startTimeout):
        self._detector.setSubject(self._subject)
        self._detector.setStream(self._stream)
        self._detector.setOutputQ(self._eventsQ)
        self._detector.setStreamDetectorThread(startTimeout)

    def startThreads(self):
        self._detector.start()

    def stopThreads(self, timeout):
        alive = self._detector.stop(timeout)
        if not alive:
            logger.debug("Stopped stream detector wrapper for stream {}".format(self._stream.name))