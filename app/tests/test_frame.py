import unittest
from video.frame import Frame
import numpy as np

class TestFrame(unittest.TestCase):

    @classmethod
    def setup_class(self):
        self.emptyFrame = Frame(np.empty([0,3]), "dummyStream")

    def test_EmptyFrame(self):
        self.assertFalse(self.emptyFrame.frame.any())

    