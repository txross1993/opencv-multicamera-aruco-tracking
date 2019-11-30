import unittest
from detection_pipeline.events_processor.abstract_events_processor import AbstractEventsProcessor
from queue import Queue
import logging
from time import sleep
from os import environ

class EventsProcessorImpl(AbstractEventsProcessor):

    def processEvent(self, event):
        self.putOutputQ(event)

class TestEventsProcessor(unittest.TestCase):

    @classmethod
    def setup_class(self):
        environ['PROCESSOR_SLEEP']="0.1"
        

    def test_setEventQueue(self):
        eventsProcessor = EventsProcessorImpl()
        eventsQueue = Queue()
        eventsProcessor.setEventQueue(eventsQueue)
        self.assertEqual(eventsQueue, eventsProcessor.eventQueue)

    def test_ProcessorThread_unsetQ(self):
        eventsProcessor = EventsProcessorImpl()
        eventsProcessor.setProcessorThread(2)
        eventsProcessor.start()
        # No input Q was set, so event should not be set and thread should not be running
        self.assertEqual(eventsProcessor.processorThread.is_alive(), False)
       
    def test_ProcessorThread_setQ(self):
        eventsProcessor = EventsProcessorImpl()
        q = Queue()
        eventsProcessor.setEventQueue(q)
        eventsProcessor.setProcessorThread(2)
        eventsProcessor.start()
        alive = eventsProcessor.stop(2)
        self.assertEqual(alive, False)

    def test_update(self):
        '''
        If the thread has been started and the queue is empty, ensure thread stays alive.
        Only when stop is called should the thread die
        '''
        eventsProcessor = EventsProcessorImpl()
        q = Queue()
        eventsProcessor.setEventQueue(q)
        eventsProcessor.setProcessorThread(0.2)
        eventsProcessor.start()
        eventsProcessor._inputQ.put(["item"])
        sleep(0.5) # Have to wait for timeout in the update loop
        self.assertEqual(eventsProcessor._inputQ.empty(), True)
        self.assertEqual(eventsProcessor.processorThread.is_alive(), True)

        '''
        Ensure thread stays alive even when input queue is empty
        '''
        sleep(0.2)
        self.assertEqual(eventsProcessor.processorThread.is_alive(), True)

        '''
        Ensure graceful stopping - the input queue should be emptied and processed before the processing thread exits
        '''
        eventsProcessor._inputQ.put(range(0, 100,1))
        alive = eventsProcessor.stop(2)
        self.assertEqual(eventsProcessor._inputQ.qsize(), 0)
        self.assertEqual(eventsProcessor.processorThread.is_alive(), False)





        
