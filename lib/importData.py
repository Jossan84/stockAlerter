#importData.py
#17/08/2022

import json
import yfinance as yf

def importData(fileName):
    with open(fileName) as json_file:
        data = json.load(json_file)    
    return data

def printData(data):  
    # Print the data of dictionary
    for i in data['members']:
        print("Name:", i['name'])
        print("Tikr:", i['tikr'])
        print("Currency:", i['currency'])
        print("PE:", i['minPE10Years'])
        print("Years:", i['years'])
        print("EPS:", i['eps'])
        print()
        
def getLastPrice(tikr):
    data = yf.Ticker(tikr).history(period='1d')
    return data['Close']
    
def getAnnualRateOfGrouth(eps):
    lastEarnings = eps[0]
    firstEarnings = eps[10]
    numYears = 10.0
    return pow(lastEarnings/firstEarnings, 1.0/numYears)-1
    
def getEpsValueTenYears(eps, annualRateOfGrouth):
    lastEarnings = eps[0]
    numYears = 10
    return lastEarnings * pow(1 + annualRateOfGrouth, numYears)
    
def getMarketPriceTenYears(epsValueTenYears, pe):
    return epsValueTenYears * pe
    
def getAnnualRateOfGrouthTenYears(marketPriceTenYears, currentPrice):
    numYears = 10
    return pow(marketPriceTenYears/currentPrice, 1.0/numYears)-1
    