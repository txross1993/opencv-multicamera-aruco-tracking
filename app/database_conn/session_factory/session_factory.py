from generic_base_classes.singleton import Singleton
from sqlalchemy.orm import sessionmaker, scoped_session
import logging
from util.timing import timing

logger = logging.getLogger('root'+'.' + __name__)

class SqlSession(metaclass=Singleton):
    def __init__(self):
        super().__init__()
        self._sessionFactory = None
        
    @property
    def sessionFactory(self):
        return self._sessionFactory

    def setSessionFactory(self, engine):
        logger.debug("DB Connection - Binding database engine to session factory")
        session_factory  = sessionmaker(bind=engine)
        self._sessionFactory = session_factory

    def getScopedSession(self):
        logger.info("DB Connection - Requesting database scoped session")
        some_session = scoped_session(self._sessionFactory)
        return some_session

    def removeScopedSession(self, some_session):
        logger.debug("DB Connection - Removing a scoped session")
        some_session.remove()

    def addObject(self, some_session, objectInstance):
        some_session.add(objectInstance)

    @timing
    def commitChanges(self, some_session):
        try:
            some_session.commit()
            logger.info("Committing records to database")
        except Exception as e:
            logger.error("Error occurred during databse session commit: {}.\nRolling back session".format(e))
            some_session.rollback()
        finally:
            logger.info("Closing session context: {}".format(some_session))
            some_session.close()
