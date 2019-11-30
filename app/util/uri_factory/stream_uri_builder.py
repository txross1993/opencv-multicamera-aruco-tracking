from .abstract_uri_factory import AbstractUriFactory
from database_conn.session_factory.session_factory import SqlSession
from database_conn.schema_definitions.table_loader import TableLoader
from os import environ
import logging

logger = logging.getLogger('root'+'.' + __name__)

class StreamUri(AbstractUriFactory):

    def __init__(self, streamId):
        super().__init__()
        self._streamId = streamId

        streamTblName = environ['TABLE_STREAM']
        deviceTblName = environ['TABLE_DEVICE']

        self._streamTbl = TableLoader().get_table(streamTblName)
        self._deviceTbl = TableLoader().get_table(deviceTblName)
        self._deviceId = self._queryForDeviceId()

    def _create_uri(self):
        user = self._get_username()
        passw = self._get_password() 
        uri = self._get_uri()
        logger.debug("Got stream URI for stream {}, uri {}".format(self._streamId, uri))
        return "rtsp://{}:{}@{}".format(user, passw, uri)

    def _get_password(self):
        logger.debug("Fetching camera device password from environment variable for device {}".format(self._deviceId))
        return environ["DEVICE_{}_PASS".format(self._deviceId)]

    def _get_username(self):
        logger.debug("Fetching camera device username from environment variable for device {}".format(self._deviceId))
        return environ["DEVICE_{}_USER".format(self._deviceId)]

    def _get_uri(self):
        host,path = self._queryForHostPath()
        return host+path

    def _getSqlSession(self):
        session = SqlSession().getScopedSession()
        return session

    def _queryForHostPath(self):
        session = self._getSqlSession()
        logger.debug("Starting query execution for stream_id {}, device_id {} to fetch host, path".format(self._streamId, self._deviceId))
        q = session.query(self._streamTbl.c.streamUri, self._deviceTbl.c.host).filter(self._streamTbl.c.streamId==self._streamId).join(self._deviceTbl)
        logger.debug("Finished query execution for stream_id {}, device_id {} to fetch host, path".format(self._streamId, self._deviceId))
        session.remove()
        fields = q.all()
        host = fields[0][1]
        path = fields[0][0]
        logger.debug("Retrieved host and path for stream_id {}, device_id {}".format(self._streamId, self._deviceId))
        return host,path

    def _queryForDeviceId(self):
        session = self._getSqlSession()
        logger.debug("Starting query execution for stream_id {} to fetch device id".format(self._streamId))
        q = session.query(self._streamTbl.c.cameraDeviceId).filter(self._streamTbl.c.streamId==self._streamId)
        logger.debug("Finished query execution for stream_id {} to fetch device id".format(self._streamId))
        session.remove()
        deviceId = q.all()[0][0]
        logger.debug("Retrieved device_id for stream_id {}".format(self._streamId))
        return deviceId