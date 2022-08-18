#test.py
#17/08/2022

import sys

sys.path.append( '../lib' )

from importData import importData
from importData import getLastPrice

class Test(object):
    fileName = '../data/stocksData.json'
    def __init__(self):
        self.data = None
    def run(self):
        self.testImportData()
        self.testDataIsEmpty()
        self.testDataStructure()
        self.testGetLastPrice()
    
    def testImportData(self):
        try:
            self.data = importData(self.fileName)
        except NameError:
            raise NameError
        
    def testDataIsEmpty(self):
        assert isinstance(self.data, dict), f"Not valid input data type for file: {self.fileName}"
    
    def testDataStructure(self):
        for data in self.data['members']:
            assert "name" in data, f"Key name is not in data from file: {self.fileName}"
            assert "tikr" in data, f"Key tikr is not in data from file: {self.fileName}"
            assert "currency" in data, f"Key currency is not in data from file: {self.fileName}"            
            assert "minPE10Years" in data, f"Key minPE10Years is not in data from file: {self.fileName}"
            assert "years" in data, f"Key years is not in data from file: {self.fileName}"
            assert "eps" in data, f"Key eps is not in data from file: {self.fileName}"
    
    def testGetLastPrice(self):
        try:
            data = getLastPrice("CPRT")
        except NameError:
            raise NameError