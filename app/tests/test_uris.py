import unittest
from util.uri_factory.sql_engine_uri_creator import SqlEngineUri
from util.uri_factory.stream_uri_builder import StreamUri
from os import environ, path

# Database connectivity
from database_conn.database_engine.postgres_sqlalchemy_engine import PostgresSqlEngine
from database_conn.session_factory.session_factory import SqlSession
from database_conn.schema_definitions.table_loader import TableLoader

import logging

def testingLocally():
    try:
        a = environ['TESTING_LOCAL']
        return True
    except KeyError:
        return False

class test_URI(unittest.TestCase):

    @classmethod
    def setup_class(self):
        environ['TABLE_TRACKING']= "rack_trackings"
        environ['TABLE_DEVICE']="cameras"
        environ['TABLE_STREAM']= "streams"

        self.tableList=[environ['TABLE_TRACKING'], environ['TABLE_DEVICE'], environ['TABLE_STREAM']]

    def test_SqlUri(self):

        user = "test"
        host = "test"
        port = "5432"
        database = "test"
        
        environ['DB_HOST'] = host
        
        environ["DB_USER"] = user
        environ["DB_PORT"] = port
        environ["DB_DATABASE"] = database

        expected = "{}:{}@{}:{}/{}".format(user, environ["DB_PASSWORD"], host, port, database)

        returned = SqlEngineUri().uri

        self.assertEqual(expected, returned)

    def setupDatabaseConn(self):
        environ['DB_HOST'] = "awsletechdocker01"
        environ["DB_USER"] = "postgres"
        environ["DB_PORT"] = "5432"
        environ["DB_DATABASE"] = "cvt28_v2"
        dbConn = PostgresSqlEngine()
        dbConn.setEngine()
        engine = dbConn.engine
        SqlSession().setSessionFactory(engine)
        return engine

    def setTableLoader(self, dbEngine):
        loader = TableLoader()
        loader.setTableList(self.tableList)
        loader.reflectTables(dbEngine)
        return loader

    

    @unittest.skipUnless(testingLocally(), "requires local environment variables for db connection")
    def test_StreamUri(self):
        testUser = "blah"
        testPass = "bpass"
        environ["DEVICE_6_PASS"] = testPass
        environ["DEVICE_6_USER"] = testUser
        DB_ENGINE = self.setupDatabaseConn()
        TABLE_LOADER = self.setTableLoader(DB_ENGINE)

        test_stream_id ="12"

        testUri = StreamUri(test_stream_id).uri

        expected = "rtsp://{}:{}@{}".format(testUser, testPass, "10.19.1.180/axis-media/media.amp?camera=6")

        self.assertEqual(testUri, expected)