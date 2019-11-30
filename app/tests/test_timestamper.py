from app.util import timestamper
from datetime import datetime
from unittest import TestCase
from mock import patch

class TestTimestamper(TestCase):    
    @patch.object(timestamper, 'get_utcnow')
    def test_getNow(self, mockGetUtcNow):
        mockGetUtcNow.return_value=datetime(2018, 8, 24, 18, 11, 46, 411783) #1535134306412
        now = timestamper.getNow()
        assert(now==1535134306412)