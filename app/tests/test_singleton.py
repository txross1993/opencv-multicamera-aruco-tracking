from generic_base_classes.singleton import Singleton
import unittest

class InheritingSingleton(metaclass=Singleton):
    def __init__(self, var):
        self.var = var
        super().__init__()

class Car:

    def __init__(self):
        self._color = None

    @property
    def color(self):
        return self.color

    def setColor(self, color):
        self._color = color

class NissanAltima(Car, metaclass=Singleton):

    def __init__(self):
        self._gearshift = None
        super().__init__()

    @property
    def gearshift(self):
        return self._gearshift

    def setGearshit(self, gearshift):
        self._gearshift = gearshift

class TestSingleton(unittest.TestCase):
    
    @classmethod
    def setup_class(self):
        self.instance1 = InheritingSingleton("red")
        self.instance2 = InheritingSingleton("blue")

        self.nissan1 = NissanAltima()
        self.nissan1.setColor("red")
        self.nissan1.setGearshit("manual")

        self.nissan2 = NissanAltima()
        self.nissan2.setColor("blue")
        self.nissan2.setGearshit("automatic")

    def test_assertSingletonInstance(self):
        '''
        Ensure second instantiation of a Singleton metaclass is equal to the first instance
        '''
        self.assertEqual(self.instance1, self.instance2)

    def test_doubleInheritance(self):
        ''' 
        Ensure that multiple inheritance still respects Singleton
        '''
        self.assertEqual(self.nissan1, self.nissan2)