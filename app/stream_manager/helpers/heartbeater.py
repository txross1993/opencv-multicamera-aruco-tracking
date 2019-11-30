from util import session_request
import requests
from os import environ
from threading import Thread, Event, Timer
import logging
from abc import ABCMeta, abstractmethod
import json
from json.decoder import JSONDecodeError

logger = logging.getLogger('root'+'.' + __name__)

class Heartbeater(metaclass=ABCMeta):

    def __init__(self):
        self._stop = Event()
        self._destination = None
        self._payload = None
        super().__init__()

    @property
    def destination(self):
        return self._destination
    
    def set_destination(self, host):
        self._destination = host
        logger.debug("Set heartbeat destination host: {}".format(host))

    @property
    def payload(self):
        return self._payload

    def setPayload(self, payload):
        self._payload = payload

    def send_heartbeat(self):
        if not self._stop.is_set():
            response = None
            try:
                response = session_request.requests_retry_session() \
                            .post(self._destination, timeout=1, data=self._payload)    
            except Exception as x:
                logger.warning("Orchestrator unreachable: {}".format(x.__class__.__name__))
            
            jsonified = None
            if response:
                try:
                    jsonified = json.loads(response.content)
                except (TypeError, JSONDecodeError) as e:
                    logger.error(e)
                    pass

            #logger.info("Recieved response from orchestrator: {}".format(jsonified))
            self.handleHeartbeatResponse(jsonified)
            Timer(1, self.send_heartbeat).start()


    @abstractmethod
    def handleHeartbeatResponse(self, response):
        pass