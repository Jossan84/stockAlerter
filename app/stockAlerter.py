#stockAlerter.py
#17/08/2022

import json
import yfinance as yf
import pandas as pd

class StockAlerter(object):
    def __init__(self, fileName):
        self.data = None
        self.numYears = 10
        self.fileName = fileName

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
        return pd.to_numeric(data['Close'], errors='coerce')[0]

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

    def getStocksDataMembers(self):
        self.data = self.importData(self.fileName)        
        return self.data['members']

    def getStocksDataMember(self, members):        
        return members[0]
        
    def getStockEstimationsTenYears(self):
        data = {}
        members = self.getStocksDataMembers()
        result = [dict() for i in range(len(members))]
        count = 0
        for member in members:
            data['name'] = member['name']
            data['tikr'] = member['tikr']
            data['currency'] = member['currency']
            data['currentPrice'] = self.getLastPrice(data['tikr'])
            data['annualRateOfGrouth'] = self.getAnnualRateOfGrouth(member['eps'])
            data['epsValueTenYears'] = self.getEpsValueTenYears(member['eps'], data['annualRateOfGrouth'])
            data['marketPriceTenYears'] = self.getMarketPriceTenYears(data['epsValueTenYears'], member['minPE10Years'])
            data['annualRateOfGrouthTenYears'] = self.getAnnualRateOfGrouthTenYears(data['marketPriceTenYears'], data['currentPrice'])

            result[count] = data.copy()
            count = count + 1 
        self.printEstimations(result)
        return result
    
    def printEstimations(self, result):
            for data in result:
                if data['currency'] == "dolar":
                    currencySymbol = "$"
                else:
                    currencySymbol = "€"
            
                print("-----------------------------------------------------------")
                print(data['name'] + " (" + data['tikr'] + "):")
                print("     Earnings per share have a annual rate of grouth of " + str(round(data['annualRateOfGrouth'], 4)*100) + "%, ")
                print("     with this rate the earnings per share for ten years from now will be " + str(round(data['epsValueTenYears'], 2)) + currencySymbol + ". Multiplying this for the min PE of ")
                print("     last ten years we get a market price of " + str(round(data['marketPriceTenYears'], 2)) + currencySymbol + " per share to ten years. If the current price is " + str(round(data['currentPrice'], 2)) + currencySymbol )
                print("     whe could get a annual rate of grouth of " + str(round(data['annualRateOfGrouthTenYears']*100, 2)) + "%.")            