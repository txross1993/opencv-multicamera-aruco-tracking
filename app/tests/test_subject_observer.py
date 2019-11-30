from generic_base_classes.observer import AbstractObserver
from generic_base_classes.subject import AbstractSubject
import unittest

class TestSubject(AbstractSubject):

    def __init__(self):
        super().__init__()

class TestObserver(AbstractObserver):
    def __init__(self):
        self._test = None
        super().__init__()

    def update(self, val):
        self._test = val

class TestSubjectObserver(unittest.TestCase):

    @classmethod
    def setup_class(self):
        self._subject = TestSubject()
        self._observer = TestObserver()

    def testAttach(self):
        self._subject.attach(self._observer)
        self.assertEqual(next(iter(self._subject._observers)), self._observer)    

    def testUpdate(self):
        test = "hello"
        self._subject.notify(test)
        self.assertEqual(self._observer._test, test)

    def testDetach(self):
        anotherObserver = TestObserver()
        self._subject.attach(anotherObserver)
        self._subject.detach(anotherObserver)
        assert(anotherObserver not in self._subject._observers)
        
        