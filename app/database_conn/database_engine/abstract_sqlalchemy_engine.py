from abc import ABCMeta, abstractmethod
from sqlalchemy import create_engine
from sqlalchemy.event import listens_for
import logging, os

logger = logging.getLogger('root'+'.' + __name__)

class AbstractSqlEngine(metaclass=ABCMeta):

    def __init__(self):
        super().__init__()
        self._engine = None
        

    @abstractmethod
    def _build_connection_string(self):
        pass

    @property
    def engine(self):
        return self._engine
                
    def setEngine(self):
        connStr = self._build_connection_string()
        engine = create_engine(connStr)
        self._engine = engine        
        self._add_process_guards()
    
    def _add_process_guards(self):
        """Add multiprocessing guards.

        Forces a connection to be reconnected if it is detected
        as having been shared to a sub-process.

        """

        @listens_for(self._engine, "connect")
        def connect(dbapi_connection, connection_record):
            connection_record.info['pid'] = os.getpid()

        @listens_for(self._engine, "checkout")
        def checkout(dbapi_connection, connection_record, connection_proxy):
            pid = os.getpid()
            if connection_record.info['pid'] != pid:
                logger.debug(
                    "Parent process %(orig)s forked (%(newproc)s) with an open "
                    "database connection, "
                    "which is being discarded and recreated.",
                    {"newproc": pid, "orig": connection_record.info['pid']})
                connection_record.connection = connection_proxy.connection = None
                raise Exception(
                    "Connection record belongs to pid %s, "
                    "attempting to check out in pid %s" %
                    (connection_record.info['pid'], pid)
                )

    