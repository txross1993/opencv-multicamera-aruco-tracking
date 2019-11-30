from abc import ABCMeta, abstractmethod

class AbstractUriFactory(metaclass=ABCMeta):

    """
    Specify the abstract interface for creating a stream URI
    """

    def __init__(self):
        super().__init__()
    
    @property
    def uri(self):
        return self._create_uri()

    @abstractmethod
    def _create_uri(self):
        pass

    