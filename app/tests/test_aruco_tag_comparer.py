import unittest
from os import environ
environ['LOCATION_THRESHOLD']="3"
environ['TS_THRESHOLD']="3000"

from util import timestamper
from detection_pipeline.event_struct.location_point import Point
from detection_pipeline.events_processor.helpers.aruco_tag_comparer import TagComparer
from detection_pipeline.event_struct.aruco_tag_event_struct import TagEventStruct
from detection_pipeline.events_processor.helpers.aruco_tag_states import TagComparisonStates

class TestTagComparer(unittest.TestCase):

    @classmethod
    def setup_class(self):
        #NEW
        location1 = Point()
        location1.setX(10)
        location1.setY(10)
        self.event1 = TagEventStruct()
        self.event1.setLocation(location1)
        self.event1.setSourceStream("event1-stream")
        self.event1.setTagId(110)
        self.event1.setTimestamp(timestamper.getNow())

        #UNCHANGED
        location2 = Point()
        location2.setX(10)
        location2.setY(12)
        self.event2 = TagEventStruct()
        self.event2.setLocation(location2)
        self.event2.setSourceStream("event2-stream")
        self.event2.setTagId(110)
        self.event2.setTimestamp(self.event1.timestamp)

        #ERR
        location3 = Point()
        location3.setX(10)
        location3.setY(15)
        self.event3 = TagEventStruct()
        self.event3.setLocation(location3)
        self.event3.setSourceStream("event2-stream")
        self.event3.setTagId(110)
        self.event3.setTimestamp(self.event1.timestamp)

        #UNCHANGED
        location5 = Point()
        location5.setX(10)
        location5.setY(12)
        self.event5 = TagEventStruct()
        self.event5.setLocation(location5)
        self.event5.setSourceStream("event1-stream")
        self.event5.setTagId(110)
        self.event5.setTimestamp(self.event1.timestamp)

        #UPDATED
        location4 = Point()
        location4.setX(10)
        location4.setY(15)
        self.event4 = TagEventStruct()
        self.event4.setLocation(location4)
        self.event4.setSourceStream("event4-stream")
        self.event4.setTagId(110)
        self.event4.setTimestamp(self.event1.timestamp+3001)

    def test_unchanged(self):
        state = TagComparer(self.event1, self.event5).compare()
        self.assertEqual(state,TagComparisonStates.UNCHANGED)

    def test_err(self):
        state = TagComparer(self.event1, self.event3).compare()
        self.assertEqual(state,TagComparisonStates.ERR)

    def test_updated(self):
        state = TagComparer(self.event1, self.event4).compare()
        self.assertEqual(state,TagComparisonStates.UPDATED)

        