from abc import ABCMeta, abstractmethod
from threading import Thread
from queue import Queue, Empty
import logging
from time import sleep
from os import environ
from util.counts_per_sec import CountsPerSec as CPS

logger = logging.getLogger('root'+'.' + __name__)

class AbstractReporter(metaclass=ABCMeta):

    def __init__(self):
        super().__init__()
        self._reporterThread = None
        self._batchSize = int(environ['REPORTER_BATCH_SIZE'])
        self._stopped = False
        self._inputQ = None
        self._numEventsReported = 0
        self.sleep_time=float(environ['REPORTER_SLEEP'])

    @property
    def inputQ(self):
        return self._inputQ

    def setInputQ(self, inputQ):
        self._inputQ = inputQ

    @property
    def batchSize(self):
        return self._batchSize

    def setBatchSize(self, batchSize):
        self._batchSize = batchSize

    @property
    def reporterThread(self):
        return self._reporterThread

    def setReporterThread(self, timeout):
        self._reporterThread =  Thread(name='ReporterThread', target=self.getEvents, args=(timeout,))
        logger.debug("Reporting thread instantiated")

    def start(self):
        if self._batchSize and self._inputQ:
            if not self._reporterThread.is_alive():
                try:
                    self._reporterThread.start()
                    logger.debug("STARTED - Reporting thread started")
                except RuntimeError:
                    logger.debug("Reporting thread has aready been started")
        else:
            logger.error('Unable to set reporter thread until batch size property and input queue are set!')

    def stop(self, timeout):
        self._inputQ.join()
        self._stopped = True
        if self._reporterThread.is_alive():
            self._reporterThread.join(timeout)
            logger.debug("STOPPED - Reporter thread sent signal to join on a timeout. Alive? {}".format(self._reporterThread.is_alive()))
        return self._reporterThread.is_alive()

    def getEvents(self, timeout):
        logger.debug("ENTERING - Entering reporting loop")
        cps = CPS().start()
        while not self._stopped:
            #logger.info("STILL RUNNING - Events reporter still running. Number of events reported: {}".format(self._numEventsReported))
            sleep(self.sleep_time)
            try:
                event = self._inputQ.get_nowait()
                logger.info("REPORTER QUEUE SIZE {}".format(self._inputQ.qsize()))
                self.reportEvents(event)
                self._inputQ.task_done()
                self._numEventsReported+=1
            except Empty:
                continue
            logger.info(
            	"Loop iterations/sec: {:.0f}".format(cps.countsPerSec()))
            cps.increment()

    @abstractmethod
    def reportEvents(self, inputEvent):
        pass