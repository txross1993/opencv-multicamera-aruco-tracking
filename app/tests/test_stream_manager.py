from os import environ
environ['LOCATION_THRESHOLD']="3"
environ['TS_THRESHOLD']="3000"
import unittest
from stream_manager.tag_stream_manager import TagStreamManager
from mock import patch
import json
class TestStreamManager(unittest.TestCase):

    @classmethod
    def setup_class(self):
        
        self.maxItems = 5
        self.manager = TagStreamManager('127.0.0.1', self.maxItems)
        self.test_stream_id_1 = 10
        self.test_stream_id_2 = 11

    def test_initMaxItems(self):        
        self.assertEqual(self.manager._max, self.maxItems)

    def test_initMaxDict(self):
        expectedDict = {1: None, 2: None, 3: None, 4: None, 5: None}
        self.assertEqual(self.manager._managed_items_dict, expectedDict)

    def test_PayloadInit(self):
        expectedPayload = json.dumps({ 'num_streams': 5, 'streams': [], 'pod_name': environ['HOSTNAME'] })
        self.manager.setPayload(self.manager.getStreamMetricPayload())
        self.assertEqual(self.manager.payload, expectedPayload)

    def test_orchestrator_endpoints(self):
        assert(self.manager._rejected_stream_endpoint=='127.0.0.1/rejected_stream')
        assert(self.manager._managed_stream_endpoint=='127.0.0.1/heartbeat')

    def test_reject_stream(self):
        with patch.object(TagStreamManager, 'send_rejected_stream_response', autospec=True) as mock_send_stream_response:
            self.manager.reject_stream(self.test_stream_id_1)
            assert(self.test_stream_id_1 in self.manager._reject_streams)

    def test_rejected_stream_payload(self):
        returned_payload = self.manager.rejected_stream_payload(self.test_stream_id_1)
        expected_payload = json.dumps({'pod_name': environ['HOSTNAME'],
                            'stream': self.test_stream_id_1 })
        self.assertEqual(returned_payload, expected_payload)

    def test_is_reject(self):
        with patch.object(TagStreamManager, 'send_rejected_stream_response', autospec=True) as mock_send_stream_response:
            self.manager.reject_stream(self.test_stream_id_1)

        self.assertTrue(self.manager.is_reject(self.test_stream_id_1))
        self.assertFalse(self.manager.is_reject(self.test_stream_id_2))

    def test_remove_reject(self):
        with patch.object(TagStreamManager, 'send_rejected_stream_response', autospec=True) as mock_send_stream_response:
            self.manager.reject_stream(self.test_stream_id_1)

        self.manager.remove_reject(self.test_stream_id_1)
        self.manager.remove_reject(self.test_stream_id_2)

        assert(self.manager._reject_streams==set())