from .abstract_sqlalchemy_engine import AbstractSqlEngine
from generic_base_classes.singleton import SingletonImpl
from util.uri_factory.sql_engine_uri_creator import SqlEngineUri
from util import metaclassResolver

class PostgresSqlEngine(metaclassResolver.metaclass_resolver(AbstractSqlEngine, SingletonImpl)):

    def __init__(self):
        super().__init__()
    
    def _build_connection_string(self):
        uri = SqlEngineUri().uri
        connStr="postgresql+psycopg2://{}".format(uri)
        return connStr