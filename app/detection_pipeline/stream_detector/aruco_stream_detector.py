
from .abstract_stream_detector import AbstractStreamDetector
from detection_pipeline.detection_subject.aruco_tag import ArucoTag
from .detector_exceptions import InvalidDetectionSubject
from detection_pipeline.event_struct.aruco_tag_event_struct import TagEventStruct
from detection_pipeline.event_struct.location_point import Point
from util import point_transformation, timestamper
from video.frame import Frame
import cv2.aruco as aruco
import logging
import numpy as np
from util.timing import timing

logger = logging.getLogger('root'+'.' + __name__)

class ArucoTagStreamDetector(AbstractStreamDetector):

    def __init__(self):
        super().__init__()        

    # Implement Abstract Methods:

    def verifySubjectType(self):
        if not isinstance (self._subject, ArucoTag):
            raise InvalidDetectionSubject(expected=ArucoTag.__name__, actual=self._subject.__name__)    

    @timing
    def get_events(self, frame):
        events = []
        rawDetections = self._getIdsAndCorners(frame)
        if rawDetections:
            for tagId, corners in rawDetections.items():
                sourceStream = frame.sourceStream
                location = ArucoTagStreamDetector._getLocation(corners, frame.transformationMtx)
                event = self.composeEventStruct(tagId, sourceStream, location)
                events.append(event)
                logging.info("Event detected: {}".format(event.toDict()))
        return events

    def composeEventStruct(self, tagId, sourceStream, location):
        event = TagEventStruct()
        event.setTagId(tagId)
        event.setTimestamp(timestamper.getNow())
        event.setLocation(location)
        event.setSourceStream(sourceStream)
        return event

    # Define how abstract method gets implemented

    def _getIdsAndCorners(self, frame:Frame)->dict:
        """ Get the dictionary of {tagId: corners}
        
        Arguments:
            frame {Frame} -- video stream data
        
        Returns:
            dict -- {tagId: corners}
        """
        rawDetectionsDict = dict()
        grayFrame = frame.get_grayUndistortedFrame()
        dictionary, parameters = self._subject.features
        corners, ids, _ = aruco.detectMarkers(grayFrame, dictionary, parameters=parameters) # The underscore represents rejectedImgPts, which we're not concerned with
        if corners and ids.all():
            for cornerSet, tagId in zip(corners,ids):
                tag = tagId[0]
                extractedCorners = cornerSet[0]
                rawDetectionsDict.update({tag: extractedCorners})        
        return rawDetectionsDict

    @staticmethod
    def _getLocation(corners, transformationMtx) -> list:
        midpoint = ArucoTagStreamDetector._calculateMidpoint(corners)
        roomLocation = ArucoTagStreamDetector._getRoomCoordinates(midpoint, transformationMtx)
        location = Point()
        location.setX(roomLocation[0])
        location.setY(roomLocation[1])
        return location

    @staticmethod
    def _getRoomCoordinates(midpoint:list, transformationMtx) -> list:
        return point_transformation.transformPoint(midpoint, transformationMtx)

    @staticmethod
    def _calculateMidpoint(corners):
        x1 = corners[0].item(0)
        x2 = corners[2].item(0)
        y1 = corners[0].item(1)
        y2 = corners[2].item(1)

        midpoint_x = round((x2+x1)/2, 2)
        midpoint_y = round((y2+y1)/2, 2)
        
        return [midpoint_x, midpoint_y]