#test.py
#17/08/2022

import sys

sys.path.append( '../app' )

from stockAlerter import StockAlerter


class Test(object):
    fileName = '../data/stocksData.json'
    def __init__(self):
        self.data = None
    def run(self):
        self.testImportData()
        self.testDataIsEmpty()
        self.testDataStructure()
        self.testGetLastPrice()
        self.testGetAnnualRateOfGrowth()
        self.testGetEpsValueTenYears()
        self.testGetMarketPriceTenYears()
        self.testGetAnnualRateOfGrowthTenYears()
        self.testGetStockEstimationsTenYears()
        
    def testImportData(self):
        try:
            stockAlerter = StockAlerter(self.fileName)
            self.data = stockAlerter.importData(self.fileName)
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
            stockAlerter = StockAlerter(self.fileName)
            data = stockAlerter.getLastPrice("CPRT")
        except NameError:
            raise NameError
         
    def testGetAnnualRateOfGrowth(self):
        eps = [ 2.63, 2.36, 1.90, 1.47, 0.98, 0.53, 0.38, 0.28, 0.15, 0.11, 0.02, 0.02 ]
        
        stockAlerter = StockAlerter(self.fileName)
        result = stockAlerter.getAnnualRateOfGrowth(eps)
        assert result == 0.628893068687475, "Wrong implementation for get annual rate of grouth"
        
    def testGetEpsValueTenYears(self):
        eps = [ 2.63, 2.36, 1.90, 1.47, 0.98, 0.53, 0.38, 0.28, 0.15, 0.11, 0.02, 0.02 ]
        annualRateOfGrowth = 0.628893068687475
        
        stockAlerter = StockAlerter(self.fileName)
        result = stockAlerter.getEpsValueTenYears(eps, annualRateOfGrowth)
        assert result == 345.8450000000001, "Wrong implementation for get eps value to 10 years"

    def testGetMarketPriceTenYears(self):
        epsValueTenYears = 345.8450000000001
        pe = 10
        
        stockAlerter = StockAlerter(self.fileName)
        result = stockAlerter.getMarketPriceTenYears(epsValueTenYears, pe)
        assert result == 3458.4500000000007, "Wrong implementation for get market price to 10 years"
        
    def testGetAnnualRateOfGrowthTenYears(self):
        marketPriceTenYears = 3458.4500000000007
        currentPrice = 229.83
        
        stockAlerter = StockAlerter(self.fileName)
        result = stockAlerter.getAnnualRateOfGrowthTenYears(marketPriceTenYears, currentPrice)
        assert result == 0.3114371389976238, "Wrong implementation for get annual rate of grouth to 10 years"
        
    def testGetStockEstimationsTenYears(self):
        try:
            stockAlerter = StockAlerter(self.fileName)
            result = stockAlerter.getStockEstimationsTenYears()
        except NameError:
            raise NameError
        
