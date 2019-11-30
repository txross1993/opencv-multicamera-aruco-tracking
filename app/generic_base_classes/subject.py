from abc import ABCMeta, abstractmethod
from generic_base_classes.observer import AbstractObserver

class AbstractSubject(metaclass=ABCMeta):

    def __init__(self):
        super().__init__()
        self._observers = set()

     # Set up observer pattern

    def attach(self, observer):
        if not isinstance(observer, AbstractObserver):
            raise TypeError("Detection processor not derived from AbstractObserver")
        self._observers |= {observer}

    def detach(self, observer):
        self._observers -= {observer}

    def notify(self, value=None):
        for observer in self._observers:
            if value:
                observer.update(value)
            else:
                observer.update()