from .abstract_reporter import AbstractReporter
from database_conn.session_factory.session_factory import SqlSession
from sqlalchemy.orm.session import Session
from detection_pipeline.event_struct.aruco_tag_event_struct import TagEventStruct
from .helpers.get_tracking_record import TagEventRecord
import logging
from util.timing import timing

logger = logging.getLogger('root'+'.' + __name__)

class ArucoTagReporter(AbstractReporter):

    def __init__(self):
        super().__init__()
        self.batch = []
        self._scoped_session = SqlSession().getScopedSession()
        
    def setDbSession(self):
        self._scoped_session = SqlSession().getScopedSession()

    def addToSession(self, record):
        SqlSession().addObject(self._scoped_session, record)
        logger.info("Added record to sql session: tag {}, stream {}, coordinates {}, time {}".format(record.tagId, record.streamStreamId, (record.roomCoordX, record.roomCoordY), record.ts))

    def commit(self):
        SqlSession().commitChanges(self._scoped_session)     

    @timing
    def reportEvents(self, inputEvent:TagEventStruct):
        logging.info("Reporting event: {}".format(inputEvent.toDict()))
        record = TagEventRecord().getRecord(inputEvent)

        self.batch.append(record)

        if self.batchSizeReached():
            self.setDbSession()
            self.commitBatchedRecords()

    def batchSizeReached(self) -> bool: 
        return len(self.batch) >= self._batchSize

    def commitBatchedRecords(self):
        for record in self.batch:
            self.addToSession(record)
        self.batch.clear()
        self.commit()

    