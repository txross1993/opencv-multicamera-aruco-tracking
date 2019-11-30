from .abstract_detection_subject import AbstractDetectionSubject
from util import file_loader as pathfinder
from cv2 import aruco as aruco
import logging

logger = logging.getLogger('root'+'.' + __name__)

class ArucoTag(AbstractDetectionSubject):

    def __init__(self):
        super().__init__()

    def loadFeatures(self, dictionaryLocation):
        self._getDictionary(dictionaryLocation)
        self._getParameters()

    def _getDictionary(self, dictionaryLocation):

        logger.debug("Loading aruco tag dictionary from file: {}".format(dictionaryLocation))

        dictionaryFile = pathfinder.findRelativeFilePath(dictionaryLocation)
        unpickeldDictionary = pathfinder.unpickle(dictionaryFile)

        logger.debug("Successfully unpickled the aruco dictionary")
        
        logger.debug("Loading custom aruco tag dictionary")
        dictionary = aruco.custom_dictionary(2,2)

        logger.debug("Aruco dictionary - Adding marker size")
        dictionary.markerSize = unpickeldDictionary['markerSize']

        logger.debug("Aruco dictionary - Adding bytes list")
        dictionary.bytesList = unpickeldDictionary['bytesList']

        logger.debug("Aruco dictionary - Adding max correction bits")
        dictionary.maxCorrectionBits = unpickeldDictionary['maxCorrectionBits']
        
        self.addFeature(dictionary)

    def _getParameters(self):
        self.addFeature(aruco.DetectorParameters_create())
