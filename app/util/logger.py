#from generic_base_classes.singleton import Singleton
import logging
import sys

class Logger():
    def setup_logger(self, logLevel):        
        level = logging.getLevelName(logLevel)
        root = logging.getLogger('root')
        root.setLevel(level)
        root.propagate = True
        
        if not root.handlers:
            ch = logging.StreamHandler(sys.stdout)
            ch.setLevel(level)
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            ch.setFormatter(formatter)
            root.addHandler(ch)
