#stockAlerter.py
#17/08/2022

import json
import yfinance as yf

class StockAlerter(object):
    def __init__(self):
        self.data = None
        self.numYears = 10

    def importData(self, fileName):
        with open(fileName) as json_file:
            data = json.load(json_file)    
        return data

    def printData(self):  
        # Print the data of dictionary
        for i in self.data['members']:
            print("Name:", i['name'])
            print("Tikr:", i['tikr'])
            print("Currency:", i['currency'])
            print("PE:", i['minPE10Years'])
            print("Years:", i['years'])
            print("EPS:", i['eps'])
            print()

    def getLastPrice(self, tikr):
        data = yf.Ticker(tikr).history(period='1d')
        return data['Close']

    def getAnnualRateOfGrouth(self, eps):
        lastEarnings = eps[0]
        firstEarnings = eps[10]
        return pow(lastEarnings/firstEarnings, 1.0/self.numYears)-1

    def getEpsValueTenYears(self, eps, annualRateOfGrouth):
        lastEarnings = eps[0]
        return lastEarnings * pow(1 + annualRateOfGrouth, self.numYears)
    
    def getMarketPriceTenYears(self, epsValueTenYears, pe):
        return epsValueTenYears * pe
    
    def getAnnualRateOfGrouthTenYears(self, marketPriceTenYears, currentPrice):
        return pow(marketPriceTenYears/currentPrice, 1.0/self.numYears)-1
