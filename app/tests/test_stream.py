import unittest
from mock import patch
from video.stream import VideoStream
from util import file_loader
import numpy as np
import logging
from time import sleep
from os import environ, path
from video.stream_status import StreamStatus

class TestStream(unittest.TestCase):

    @classmethod
    def setup_class(self):
        environ['TABLE_STREAM'] = "streams"
        environ['TABLE_DEVICE'] = "cameras"

    def test_get_intrinsic_calibration(self):
        with patch.object(VideoStream, 'getUri') as mockGetUri:
            mockGetUri.return_value = environ['TEST_STREAM']
            stream = VideoStream(10)
            returned_calibration=stream._getIntrinsicCalibrationFile('data/intrinsic_calibration')
            expected_calibration=file_loader.unpickle(file_loader.findRelativeFilePath('data/intrinsic_calibration' +'/M3058'))
            self.assertEqual(all(returned_calibration),all(expected_calibration))


    def testStream(self):
        with patch.object(VideoStream, 'getUri') as mockGetUri:
            mockGetUri.return_value = environ['TEST_STREAM']
            logging.debug(environ['TEST_STREAM'])
            stream = VideoStream(1)
            stream.setupStream()
            stream.start()
            sleep(1)
            stream.stop()
            assert(any(stream._metrics))

    def test_get_transformation_mtx(self):
        with patch.object(VideoStream, 'getUri') as mockGetUri:
            mockGetUri.return_value = environ['TEST_STREAM']
            test_stream_id_42 = VideoStream(42)
            test_stream_id_42.set_transformation_matrix()
            assert(test_stream_id_42.status==StreamStatus.REJECTED)