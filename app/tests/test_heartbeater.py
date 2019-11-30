import unittest
from mock import patch
from stream_manager.helpers.heartbeater import Heartbeater
from time import sleep

class HeartbeaterImpl(Heartbeater):

    def __init__(self):
        self.set_destination('127.0.0.1:8080')
        self._talliedResponses = 0
        super().__init__()

    def handleHeartbeatResponse(self, response):
        self._talliedResponses += 1


class TestHeartbeater(unittest.TestCase):
    
    def test_SendHeartbeat(self,):
        heartbeater = HeartbeaterImpl()
        heartbeater.send_heartbeat()
        sleep(2)
        assert(heartbeater._talliedResponses > 1)
        heartbeater._stop.set()