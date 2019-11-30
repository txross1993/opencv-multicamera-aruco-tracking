from .abstract_detection_subject import AbstractDetectionSubject
import logging

logger = logging.getLogger('root'+'.' + __name__)

class NullSubject(AbstractDetectionSubject):

    def __init__(self):
        logger.debug("Null subject instantiated")
        super().__init__()
    
    def loadFeatures(self):
        pass