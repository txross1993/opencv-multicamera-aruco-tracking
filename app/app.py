def main():
    # Load configuration
    # from util.config import Config
    # utilities
    from os import environ, path
    
    # def loadConfig():
    #     config = Config()
    #     config.load_configs(path.dirname(path.realpath(__file__))+'/util/configs')
    #     return config.config

    # CONFIG = loadConfig()

    # Load Logger
    from util.logger import Logger
    Logger().setup_logger(environ['LOG_LEVEL'])

    #Load other modules AFTER loading Logger
    # Database connectivity
    from database_conn.database_engine.postgres_sqlalchemy_engine import PostgresSqlEngine
    from database_conn.session_factory.session_factory import SqlSession
    from database_conn.schema_definitions.table_loader import TableLoader
    from detection_pipeline.reporter.helpers.get_tracking_record import TagEventRecord

    # Stream Manager
    from stream_manager.tag_stream_manager import TagStreamManager

    

    ##### Initialize components #####
    

    def setupDatabaseConn():
        dbConn = PostgresSqlEngine()
        dbConn.setEngine()
        engine = dbConn.engine
        SqlSession().setSessionFactory(engine)
        return engine

    def setTableLoader(listOfTables, dbEngine):
        loader = TableLoader()
        loader.setTableList(listOfTables)
        loader.reflectTables(dbEngine)
        return loader

    def setTagEventRecordSchema(tracking_tbl_name):
        tag_event_record = TagEventRecord()
        tag_event_record.setTrackingTable(tracking_tbl_name)
        tag_event_record.setTrackingTableColumns()

    DB_ENGINE = setupDatabaseConn()
    tableList = [environ['TABLE_TRACKING'],
                 environ['TABLE_DEVICE'],
                 environ['TABLE_STREAM'] ]

    TABLE_LOADER = setTableLoader(tableList, DB_ENGINE)

    setTagEventRecordSchema(tableList[0])

    STREAM_MANAGER = TagStreamManager(environ['ORCHESTRATOR'],
                                      int(environ['MAX_MANAGED_STREAMS']))
    STREAM_MANAGER.setupSubject(environ['ARUCO_DICT'])
    STREAM_MANAGER.initializeProcessingPipeline()
    
    STREAM_MANAGER.setPayload(STREAM_MANAGER.getStreamMetricPayload())
    STREAM_MANAGER.send_heartbeat()

if __name__=='__main__':
    main()
    

    