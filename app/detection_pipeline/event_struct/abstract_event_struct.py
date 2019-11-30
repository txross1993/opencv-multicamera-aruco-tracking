from abc import ABCMeta, abstractmethod

class AbstractEventStruct(metaclass=ABCMeta):

    def __init__(self):     
        super().__init__()

    @abstractmethod
    def __eq__(self, other):
        """ Implement equality parameters """

    @abstractmethod
    def toDict(self):
        """ Implement """