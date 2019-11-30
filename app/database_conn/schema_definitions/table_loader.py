from sqlalchemy.engine import Engine
from sqlalchemy.schema import MetaData
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.exc import UnboundExecutionError
from generic_base_classes.singleton import Singleton
from sqlalchemy import Table
from sqlalchemy.ext.declarative import declarative_base
from .dataTypeMap import DatatypeMapper
import logging

logger = logging.getLogger('root'+'.' + __name__)


class TableLoader(metaclass=Singleton):
    def __init__(self):
        self.tables = []
        self._reflectedTables = {}
        self.meta = None
    
    def setTableList(self, tables:list):
        self.tables = tables
        
    def reflectTables(self, engine:Engine):
        self.meta = MetaData(bind=engine)        
        logger.debug("Attempting metadata reflection for tables")
        try:
            self.meta.reflect()
            self.set_base()
            for table in self.tables:
                self._reflectedTables.update({(table,self.meta.tables[table])})
                logger.debug("Successfully reflected table {}".format(table))
        except UnboundExecutionError as e:
            logger.error(e)
            raise(e)
    
    def get_table(self, table_name):
        try:
            tbl = self._reflectedTables[table_name]
        except KeyError:
            logger.error("Unable to load {}, Table not found in reflected table metadata!".format(table_name))
            tbl = None
        return tbl

    def set_base(self):
        self.Base = automap_base(metadata=self.meta)
        self.Base.prepare()

    def get_table_class(self, table_name):
        ''' Load a class to create objects for a table based on loaded metadata
        
        Arguments:
            table_name {[str]} -- [description]
        
        Returns:
            [sqlalchemy.ext.automap] -- Automap reflected class from loaded metadata
        '''

        try:
            if table_name in self._reflectedTables.keys():
                cls = self.Base.classes[table_name]
                return cls
        except KeyError:
            logger.error('Unable to load class for table_name: {}. Table not found in reflection!'.format(table_name))

    def get_columns(self, table_class):
        '''        
        Arguments:
            table_class {[sqlalchemy.ext.automap]} -- generate from TableLoader.get_table_class
        
        Returns:
            dict() -- {column_name: column_type}
        '''

        columns = {}
        for column in table_class.__mapper__.columns:
            dataTypeClass = DatatypeMapper().getCls(column.type)
            columns[column.key] = dataTypeClass
        return columns