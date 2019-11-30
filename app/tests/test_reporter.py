import unittest
from detection_pipeline.reporter.abstract_reporter import AbstractReporter
from .test_events_processor import EventsProcessorImpl
from queue import Queue
import logging
from time import sleep
from os import environ

class ReporterImpl(AbstractReporter):

    def __init__(self):
        self.x = None
        super().__init__()

    def reportEvents(self, event):
        self.x = event

class TestReporter(unittest.TestCase):

    @classmethod
    def setup_class(self):
        environ['REPORTER_BATCH_SIZE']="1"
        environ['REPORTER_SLEEP']="0.1"
        self.reporter = ReporterImpl()
        self.reporter.setBatchSize(10)
        self.reporter.setReporterThread(0.2)
        

        self.processor = EventsProcessorImpl()
        q = Queue()
        self.processor.setEventQueue(q)
        self.reporter.setInputQ(self.processor._outputQ)
        self.processor.setProcessorThread(0.2)

    def test_assertStartFailsWhenBatchIsNotSet(self):
        self.reporter.setBatchSize(None)
        self.reporter.start()
        self.assertEqual(self.reporter.reporterThread.is_alive(), False)
        
        
    def test_attachEventsProcessor(self):
        self.reporter.setBatchSize(10)
        self.processor.start()
        self.reporter.start()        
        self.processor._inputQ.put(range(1,100,1))
        sleep(2)
        assert(self.reporter.x > 1)
        processorAlive = self.processor.stop(2)
        reporterAlive =self.reporter.stop(2)
        self.assertEqual(processorAlive, False)
        self.assertEqual(reporterAlive, False)
        
        ''' Assert all items in range 1 - 99 were processed after stop was called '''
        assert(self.reporter.x == 99)






        
