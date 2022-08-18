#test.py
#17/08/2022

import sys

sys.path.append( '../lib' )

from importData import importData
from importData import getLastPrice
from importData import getAnnualRateOfGrouth
from importData import getEpsValueTenYears
from importData import getMarketPriceTenYears
from importData import getAnnualRateOfGrouthTenYears

class Test(object):
    fileName = '../data/stocksData.json'
    def __init__(self):
        self.data = None
    def run(self):
        self.testImportData()
        self.testDataIsEmpty()
        self.testDataStructure()
        self.testGetLastPrice()
        self.testGetAnnualRateOfGrouth()
        self.testGetEpsValueTenYears()
        self.testGetMarketPriceTenYears()
        self.testGetAnnualRateOfGrouthTenYears()
        
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
         
    def testGetAnnualRateOfGrouth(self):
        eps = [ 2.63, 2.36, 1.90, 1.47, 0.98, 0.53, 0.38, 0.28, 0.15, 0.11, 0.02, 0.02 ]
        result = getAnnualRateOfGrouth(eps)
        assert result == 0.628893068687475, "Wrong implementation for get annual rate of grouth"
        
    def testGetEpsValueTenYears(self):
        eps = [ 2.63, 2.36, 1.90, 1.47, 0.98, 0.53, 0.38, 0.28, 0.15, 0.11, 0.02, 0.02 ]
        annualRateOfGrouth = 0.628893068687475
        result = getEpsValueTenYears(eps, annualRateOfGrouth)
        assert result == 345.8450000000001, "Wrong implementation for get eps value to 10 years"

    def testGetMarketPriceTenYears(self):
        epsValueTenYears = 345.8450000000001
        pe = 10
        result = getMarketPriceTenYears(epsValueTenYears, pe)
        assert result == 3458.4500000000007, "Wrong implementation for get market price to 10 years"
        
    def testGetAnnualRateOfGrouthTenYears(self):
        marketPriceTenYears = 3458.4500000000007
        currentPrice = 229.83
        result = getAnnualRateOfGrouthTenYears(marketPriceTenYears, currentPrice)
        assert result == 0.3114371389976238, "Wrong implementation for get annual rate of grouth to 10 years"