import numpy as np
import cv2
import logging

from abc import ABCMeta, abstractproperty

logger = logging.getLogger('root'+'.' + __name__)

class AbstractFrame(metaclass=ABCMeta):
    pass

class NullFrame(AbstractFrame):
    pass

class Frame(AbstractFrame, object):
    def __init__(self, frame, sourceStream, mtx=None, dist=None, transformationMtx=None, newcameramtx=None, roi=None):
        self.frame = frame
        self._sourceStream = sourceStream
        self.mtx = mtx
        self.dist = dist
        self.transformationMtx = transformationMtx

        self.newcameramtx = newcameramtx
        self.roi = roi

    @property
    def sourceStream(self):
        return self._sourceStream

    @property
    def height(self):
        logger.debug("Grabbing frame height")
        return self.frame.shape[:2][0]

    @property
    def width(self):
        logger.debug("Grabbing frame width")
        return self.frame.shape[:2][1]

    # def undistort(self):
    #     try:
    #         undistorted = cv2.undistort(self.frame, self.mtx, self.dist, None, self.newcameramtx)        
    #         x,y,w,h = self.roi
    #         undistorted_frame = undistorted[y:y+h, x:x+w]
    #         #logger.debug("Successfully undistorted the frame and applied appropriate cropping on frame from stream {}".format(self._sourceStream))
    #         return undistorted_frame
    #     except Exception:
    #         logger.debug("Unable to distort frame for stream {}".format(self._sourceStream))
    #         return self.frame

    def get_grayUndistortedFrame(self):
        grayUndistortedFrame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
        logger.debug("Successfully transformed a frame to grayscale for stream {}".format(self._sourceStream))
        return grayUndistortedFrame