from .abstract_uri_factory import AbstractUriFactory
from os import environ
import logging

logger = logging.getLogger('root'+'.' + __name__)

class SqlEngineUri(AbstractUriFactory):

    def _create_uri(self): 
        logger.debug("Fetching database connectivity parameters from environment variables")
        return "{}:{}@{}:{}/{}".format(environ["DB_USER"],
                                       environ["DB_PASSWORD"],
                                       environ["DB_HOST"],
                                       environ["DB_PORT"],
                                       environ["DB_DATABASE"])
