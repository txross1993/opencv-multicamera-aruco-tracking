from abc import ABCMeta, abstractmethod
import logging

logger = logging.getLogger('root'+'.' + __name__)

class AbstractDetectionSubject(metaclass=ABCMeta):

    def __init__(self,):
        super().__init__()
        self._features = []
       

    @property
    def features(self):
        return self._features

    @abstractmethod
    def loadFeatures(self, featuresSrc):
        """ Implement """

    def addFeature(self, feature):
        logger.debug("Adding subject feature {} for subject {}".format(feature, self))
        self._features.append(feature)

    def removeFeature(self, feature):
        logger.debug("Removing subject feature {} for subject {}".format(feature, self))
        self._features.remove(feature)