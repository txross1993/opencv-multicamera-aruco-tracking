import unittest
from mock import patch, PropertyMock
from ..stream_manager.helpers.streamTuple import StreamTuple
from ..detection_pipeline.stream_detector_wrapper import StreamSubjectDetectorWrapper

class TestStreamTuple(unittest.TestCase):

    @classmethod
    @patch('detection_pipeline.stream_detector_wrapper.StreamSubjectDetectorWrapper', autospec=True)
    def setup_class(self, mockStreamWrapper):
        test = mockStreamWrapper(subject=None, detector=None, stream=None, eventsQueue= None)
        mockStreamWrapper.return_value.streamName.return_value = "hello"
        self.firstTestTuple = StreamTuple(1,test)
        self.secondTestTuple = StreamTuple(1, test)
        self.thirdTestTuple = StreamTuple(2, test)

    def test_eq(self):
        self.assertEqual(self.firstTestTuple.__eq__(self.secondTestTuple), True)

    def test_uneq(self):
        self.assertEqual(self.firstTestTuple.__eq__(self.thirdTestTuple), False)