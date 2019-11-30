from abc import ABCMeta, abstractmethod
import logging

logger = logging.getLogger('root'+'.' + __name__)

class AbstractMaxDict(metaclass=ABCMeta):
    def __init__(self):
        super().__init__()
        self._max = None
        self._managed_items_dict = None
        

    def setMax(self, n):
        logger.debug("Setting the maximum amount of dictionary items")
        self._max = n

    def setupDict(self):
        logger.debug("Setting up the maximum dictionary")
        d = dict()
        for n in range(1, self._max+1):
            d.update({n: None})
        logger.debug("Max dictionary: {}".format(d))
        self._managed_items_dict = d
        logger.debug("Max dictionary set")

    @abstractmethod
    def addToDict(self, item:tuple):
        pass
        

    def getNextEmptyKey(self):
        emptyKey = next(k for k in self._managed_items_dict.keys() if self._managed_items_dict[k] is None)
        return emptyKey

    @abstractmethod
    def isDuplicateValue(self, item) -> bool:
        pass

    @abstractmethod
    def removeFromDict(self, item):
        pass