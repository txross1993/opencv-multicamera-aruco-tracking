from abc import ABCMeta, abstractmethod

class AbstractObserver(metaclass=ABCMeta):

    def __init__(self):
        super().__init__()

    @abstractmethod
    def update(self, value=None):
        pass