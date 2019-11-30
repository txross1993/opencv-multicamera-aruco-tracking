import logging
from os import environ

logger = logging.getLogger('root'+'.' + __name__)

class Point:

    location_delta_threshold = int(environ['LOCATION_THRESHOLD'])

    logger.debug("Location delta threshold set: {}".format(location_delta_threshold))

    def __init__(self):
        self._x = None
        self._y = None

    def __cmp__(self, other):
        return any([point>=Point.location_delta_threshold for point in self.__sub__(other)])

    def __sub__(self, other):
        sub = [abs(self._x-other.x), abs(self._y-other.y)]
        return sub                                                                           

    @property
    def x(self):
        return Point.getRoundedFloat(self._x)

    def setX(self, x):
        self._x = x

    @property
    def y(self):
        return Point.getRoundedFloat(self._y)

    def setY(self, y):
        self._y = y

    @staticmethod
    def getRoundedFloat(number):
        floatingNumber = float(number)
        roundedNumber = round(floatingNumber, 2)
        return roundedNumber