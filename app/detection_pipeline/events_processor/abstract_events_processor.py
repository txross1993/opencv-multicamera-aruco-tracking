from abc import ABCMeta, abstractmethod
from threading import Thread
from queue import Queue, Empty
from generic_base_classes.subject import AbstractSubject
import logging
from time import sleep
from os import environ
from util.counts_per_sec import CountsPerSec as CPS

logger = logging.getLogger('root'+'.' + __name__)

class AbstractEventsProcessor(metaclass=ABCMeta):

    def __init__(self):
        super().__init__()
        self._inputQ = None
        self._processorThread = None
        self._stopped = False
        self._outputQ = Queue()
        self._eventsProcessed=0        
        self.sleep_time=float(environ['PROCESSOR_SLEEP'])

    @property
    def eventQueue(self):
        return self._inputQ

    def setEventQueue(self, queue:Queue):
        self._inputQ = queue
        logger.debug("Events processor input queue has been set!")

    def putOutputQ(self, item):
        #logger.debug("Put event on output queue of events processor")
        self._outputQ.put(item)

    @property
    def processorThread(self):
        return self._processorThread

    def setProcessorThread(self, timeout):
        self._processorThread =  Thread(name='EventProcessorThread', target=self.update, args=(timeout,))
        logger.debug("Events processor thread has been set!")

    def start(self):
        if self._inputQ:
            if not self._processorThread.is_alive():
                try:
                    self._processorThread.start()
                    logger.info("STARTED - Events processor thread started")
                except RuntimeError:
                    logger.info("Events processor thread has already been started")
        else:
            logger.error('Unable to start events processor: input queue has not been set!')

    def stop(self, timeout):
        logger.debug("Stop called on events processor thread")
        self._inputQ.join()
        logger.debug("Events processor input queue has been joined")
        self._stopped = True
        if self._processorThread.is_alive():
            self._processorThread.join(timeout)
            logger.debug("Called stop on events processor thread")
            logger.debug("STOPPED - Events processor thread status after stop called: {}".format(self._processorThread.is_alive()))
        return self._processorThread.is_alive()


    def update(self, timeout):
        logger.debug('ENTERING - Entering events processor loop')
        cps = CPS().start()
        while not self._stopped:
            #logger.info('STILL RUNNING - Events processor loop  {}, number of events processed {}'.format(self.__class__.__name__, self._eventsProcessed))
            sleep(self.sleep_time)
            try:
                events = self._inputQ.get_nowait()
                logger.info("PROCESSOR QUEUE SIZE {}".format(self._inputQ.qsize()))
                for event in events:
                    self.processEvent(event)
                    self._eventsProcessed+=1
                self._inputQ.task_done()
            except Empty:
                continue
            logger.info("Loop iterations/sec: {:.0f}".format(cps.countsPerSec()))
            cps.increment()
                
    @abstractmethod
    def processEvent(self, inputEvent):
        """Implement"""