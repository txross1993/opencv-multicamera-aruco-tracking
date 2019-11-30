from database_conn.database_engine.abstract_sqlalchemy_engine import AbstractSqlEngine
from database_conn.session_factory.session_factory import SqlSession
from sqlalchemy.orm import sessionmaker, scoped_session
import unittest
from mock import patch

class TestAbstractEngine(unittest.TestCase):

    @classmethod
    @patch.multiple(AbstractSqlEngine, __abstractmethods__=set())
    def setup_class(self):
        self._instance = AbstractSqlEngine()

    @patch.object(AbstractSqlEngine, '_build_connection_string')
    def test_getEngine(self, mockBuildConnStr):
        mockBuildConnStr.return_value='sqlite://'
        with patch.object(AbstractSqlEngine, '_add_process_guards') as mock_add_process_guards:
            engine = self._instance.setEngine()
            mock_add_process_guards.assert_called_once()

class TestSessionFactory(unittest.TestCase):

    @classmethod
    @patch.multiple(AbstractSqlEngine, __abstractmethods__=set())
    def setup_class(self):
        with patch.object(AbstractSqlEngine, '_build_connection_string') as mockBuildConnStr:
            mockBuildConnStr.return_value='sqlite://'
            self.engine = AbstractSqlEngine().setEngine()
        self.sessionFactory = SqlSession()        
        

    def test_setSessionFactory(self):
        self.sessionFactory.setSessionFactory(self.engine)
        scoped_session1 = self.sessionFactory.getScopedSession()
        scoped_session2 = self.sessionFactory.getScopedSession()
        self.assertNotEqual(scoped_session1, scoped_session2)
        self.sessionFactory.commitChanges(scoped_session1)
        self.sessionFactory.commitChanges(scoped_session2)
        self.sessionFactory.removeScopedSession(scoped_session1)
        self.sessionFactory.removeScopedSession(scoped_session2)

    @patch.object(scoped_session, 'add', return_value="added")
    def test_addObject(self, mock_add):
        s = self.sessionFactory.getScopedSession()
        item = "test"
        self.sessionFactory.addObject(s, item)
        mock_add.assert_called_with(item)
        self.sessionFactory.removeScopedSession(s)

    @patch.object(scoped_session, 'remove', return_value="added")
    def test_removeSession(self, mock_remove):
        s = self.sessionFactory.getScopedSession()
        self.sessionFactory.removeScopedSession(s)
        mock_remove.assert_called_once()

    @patch.object(scoped_session, 'commit')
    @patch.object(scoped_session, 'rollback')
    @patch.object(scoped_session, 'close')
    def test_commitChanges(self, mock_close, mock_rollback, mock_commit):
        s = self.sessionFactory.getScopedSession()
        self.sessionFactory.commitChanges(s)
        mock_commit.assert_called_once()
        mock_close.assert_called_once()
        mock_rollback.assert_not_called()

