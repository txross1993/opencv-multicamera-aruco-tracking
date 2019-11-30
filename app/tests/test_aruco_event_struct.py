import unittest
from util import timestamper
from os import environ

class TestArucoEvent(unittest.TestCase):

    @classmethod
    def setup_class(self):
        #initial
        environ['LOCATION_THRESHOLD']="3"
        environ['TS_THRESHOLD']="3000"
        from detection_pipeline.event_struct.aruco_tag_event_struct import TagEventStruct
        from detection_pipeline.event_struct.location_point import Point
        location1 = Point()
        location1.setX(10)
        location1.setY(10)
        self.event1 = TagEventStruct()
        self.event1.setLocation(location1)
        self.event1.setSourceStream("event1-stream")
        self.event1.setTagId(110)
        self.event1.setTimestamp(timestamper.getNow())

        #equal
        location2 = Point()
        location2.setX(10)
        location2.setY(15)
        self.event2 = TagEventStruct()
        self.event2.setLocation(location2)
        self.event2.setSourceStream("event2-stream")
        self.event2.setTagId(110)
        self.event2.setTimestamp(self.event1.timestamp)

    def assertEquality(self):
        '''
        If two events have the same tag Id, they should be equal
        '''
        self.assertEqual(self.event1.__eq__(self.event2), True)
        self.event2.setTagId(120)
        self.assertEqual(not self.event1.__eq__(self.event2), False)

class TestLocation(unittest.TestCase):

    @classmethod
    def setup_class(self):
        environ['LOCATION_THRESHOLD']="3"
        environ['TS_THRESHOLD']="3000"
        from detection_pipeline.event_struct.aruco_tag_event_struct import TagEventStruct
        from detection_pipeline.event_struct.location_point import Point
        self.location1 = Point()
        self.location1.setX(10)
        self.location1.setY(10)

        self.location2 = Point()
        

    def test_cmp_x(self):
        '''
        location1 = 10,10

        location2 = 15,10

        location2.x - location1.x >= 5 --> Return True
        '''
        self.location2.setX(15)
        self.location2.setY(10)
        self.assertEqual(self.location1.__cmp__(self.location2), True)

    def test_cmp_y(self):
        '''
        location1 = 10,10

        location2 = 10,15

        location2.y - location1.y >= 5 --> Return True
        '''
        self.location2.setX(10)
        self.location2.setY(15)
        self.assertEqual(self.location1.__cmp__(self.location2), True)

    def test_both_coords(self):
        '''
        location1 = 10,10

        location2 = 15,15

        location2.x - location1.x >= 5 --> Return True &&
        location2.y - location1.y >= 5 --> Return True
        '''
        self.location2.setX(15)
        self.location2.setY(15)
        self.assertEqual(self.location1.__cmp__(self.location2), True)

    def test_equal(self):
        '''
        location1 = 10,10

        location2 = 13,13
        '''
        self.location2.setX(13)
        self.location2.setY(14)
        self.assertEqual(self.location1.__cmp__(self.location2), True)