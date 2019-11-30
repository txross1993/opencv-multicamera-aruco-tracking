import unittest
from mock import patch
from detection_pipeline.detection_subject.abstract_detection_subject import AbstractDetectionSubject

class TestDetectionSubject(unittest.TestCase):

    @classmethod
    @patch.multiple(AbstractDetectionSubject, __abstractmethods__=set())
    def setup_class(self):
        self._detectionSubject = AbstractDetectionSubject()

    def test_addFeature(self):
        self._detectionSubject.addFeature("test")
        assert("test" in self._detectionSubject._features)    

    def test_removeFeature(self):
        self._detectionSubject.removeFeature("test")
        assert("test" not in self._detectionSubject._features)