from functools import wraps
from time import time
import logging

logger = logging.getLogger('root'+'.' + __name__)

def timing(f):
  @wraps(f)
  def wrapper(*args, **kwargs):
    start = time()
    result = f(*args, **kwargs)
    end = time()
    elapsed = (end-start)*1000
    logger.info('Elapsed time for {}: {:.5f}ms'.format(f.__qualname__, elapsed))
    return result
  return wrapper
