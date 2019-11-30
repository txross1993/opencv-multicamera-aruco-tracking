import unittest
from ..generic_base_classes.abstract_max_dict import AbstractMaxDict

class MaxMngrImpl(AbstractMaxDict):

    def __init__(self):
        self.add = "Added"
        self.dup = "Duplicate!"
        self.full = "Full!"
        super().__init__()

    def addedResponse(self):
        return self.add

    def fullResponse(self):
        return self.full

    def duplicateResponse(self):
        return self.dup

    def addToDict(self, item):
        if not self.isDuplicateValue(item):
            try:
                k = self.getNextEmptyKey()
                self._managed_items_dict.update({k:item})
                return self.addedResponse()
            except:
                return self.fullResponse()
        else:
            return self.duplicateResponse()

    def isDuplicateValue(self, item):
        return(item in self._managed_items_dict.values())

    def removeFromDict(self, item):
        for k,v in self._managed_items_dict.items():
            if item == v:
                self._managed_items_dict.update({k: None})

class TestMaxMngr(unittest.TestCase):

    @classmethod
    def setup_class(self):
        self._max = 5
        self.Tester = MaxMngrImpl()        
        self.Tester.setMax(self._max)
        self.Tester.setupDict()

    def test_setMax(self):
        self.assertEqual(self.Tester._max,self._max)

    def test_setDict(self):
        self.Tester._managed_items_dict = None
        self.Tester.setupDict()
        expected = {1:None, 2:None, 3:None, 4:None, 5:None}
        self.assertEqual(self.Tester._managed_items_dict, expected)

    def test_addToDict_hasOpenSlot(self):
        self.Tester._managed_items_dict = {1:None, 2:None, 3:None, 4:None, 5:None}
        item = 1
        self.Tester.addToDict(item)
        expected = {1:1, 2:None, 3:None, 4:None, 5:None}
        self.assertEqual(self.Tester._managed_items_dict, expected)

    def test_getNextemptyKey(self):
        expected = 2
        returned = self.Tester.getNextEmptyKey()
        self.assertEqual(returned, expected)

    def test_addToDict_full(self):
        self.Tester._managed_items_dict = {1:1, 2:2, 3:3, 4:4, 5:5}
        expected = self.Tester.full
        result = self.Tester.addToDict(6)
        self.assertEqual(expected, result)

    def test_addToDict_dup(self):
        self.Tester._managed_items_dict = {1:1, 2:2, 3:3, 4:4, 5:5}
        expected = self.Tester.dup
        result = self.Tester.addToDict(5)
        self.assertEqual(expected, result)

    def test_removeFromDict(self):
        self.Tester._managed_items_dict = {1:1, 2:2, 3:3, 4:4, 5:5}
        expected = {1:1, 2:2, 3:3, 4:4, 5:None}
        self.Tester.removeFromDict(5)
        result = self.Tester._managed_items_dict
        self.assertEqual(expected, result)

    def test_removeNonexistentValue(self):
        self.Tester._managed_items_dict = {1:1, 2:2, 3:3, 4:4, 5:5}
        expected = {1:1, 2:2, 3:3, 4:4, 5:5}
        self.Tester.removeFromDict(6)
        result = self.Tester._managed_items_dict
        self.assertEqual(expected, result)