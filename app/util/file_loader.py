from os import path, walk
from pickle import load, UnpicklingError
import logging

ROOT_PATH = path.abspath(path.join(path.dirname(__file__), '..'))

logger = logging.getLogger('root'+'.' + __name__)


def findRelativeFilePath(relpath):  
    
    targetFile = path.abspath(path.join(ROOT_PATH, relpath))

    if path.exists(targetFile):
        return targetFile
    else:
        raise FileNotFoundError

def walkDir(reldir):
    relFiles = []
    for root, dirs, files in walk(path.abspath(path.join(ROOT_PATH, reldir))):
        for filename in files:
            relFiles.append(filename)
    return relFiles

def unpickle(targetFile):
    with open(targetFile, mode='rb') as b:
        try:
            unpickled = load(b, encoding='latin1')
        except (ValueError, UnpicklingError) as e:
            logger.error(e)
            raise(e)
        b.close()

    return unpickled