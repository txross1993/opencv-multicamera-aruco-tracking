from .events_processor.abstract_events_processor import AbstractEventsProcessor
from .reporter.abstract_reporter import AbstractReporter
from queue import Queue
import logging 

logger = logging.getLogger('root'+'.' + __name__)

class ProcessorReporterWrapper:
    '''
    Use this wrapper to correctly instantiate the events processor and reporter.
    The input queuue for the processor should be the same as the stream-detector output queue.
    The reportingQ is the processor's output queue and the reporter's input queue.
    '''


    def __init__(self, processor:AbstractEventsProcessor,
                       processingQ: Queue,
                       reporter:AbstractReporter,
                       startTimeout):

        self._processor = processor
        self.setupProcessor(processingQ, startTimeout)
        

        self._reporter = reporter
        self.setupReporter(startTimeout)

        ''' If at least one of the threads is dead, then _stopped==True '''
        self._stopped = not all([self._processor._processorThread.is_alive(), # if is_alive()==False, then the thread is stopped
                                 self._reporter._reporterThread.is_alive()])

    def setupProcessor(self, processingQ, startTimeout):
        self._processor.setEventQueue(processingQ)
        self._processor.setProcessorThread(startTimeout)
    
    def setupReporter(self, startTimeout):
        self._reporter.setInputQ(self._processor._outputQ)
        self._reporter.setReporterThread(startTimeout)

    def start(self):
        logger.info("STARTING processor and reporter via wrapper")
        self._processor.start()
        self._reporter.start()

    def stop(self, timeout):
        logger.info("STOPPING processor and reporter via wrapper")
        self._processor.stop(timeout)               
        self._reporter.stop(timeout)