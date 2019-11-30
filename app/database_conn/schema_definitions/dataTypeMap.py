from sqlalchemy.sql.sqltypes import INTEGER, BIGINT, VARCHAR, NUMERIC
import logging

logger = logging.getLogger('root'+'.' + __name__)

class DatatypeMapper():

    _typeMap = {
        'INTEGER': int,
        'BIGINT': int,
        'VARCHAR': str,
        'NUMERIC': float
    }
    
    @staticmethod
    def getCls(sqlType):
        sqlType = sqlType.__class__.__name__
        try:
            cls = DatatypeMapper._typeMap[sqlType]
        except KeyError:
            logger.warning("Unknown datatype for datatype mapper: {}. Defaulting to STRING type".format(sqlType))
            cls = str
        return cls