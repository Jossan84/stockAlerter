#stockAlerter.py
#17/08/2022

import os
import re
import json
import smtplib
import requests
import numpy as np
import pandas as pd
import yfinance as yf
from datetime import datetime
from email.message import EmailMessage
from bs4 import BeautifulSoup
from threading import Event


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

    def estimateCoefficients(self, x, y):
        # Number of observations/points
        n = np.size(x)

        # Mean of x and y vector
        m_x = np.mean(x)
        m_y = np.mean(y)

        # Calculating cross-deviation and deviation about x
        SS_xy = np.sum(y * x) - n * m_y * m_x
        SS_xx = np.sum(x * x) - n * m_x * m_x

        # Calculating regression coefficients
        b1 = SS_xy / SS_xx
        b0 = m_y - b1 * m_x

        return b0, b1

    def getLastEarningPerShareCorrected(self, eps):
        # Linear regression
        x = np.array(list(range(1, len(eps) + 1)))
        y = np.array(eps)
        a = self.estimateCoefficients(x, y)

        #  Pick last value
        epsCorrected = a[0] + a[1] * x
        return epsCorrected[0].item()

    def getLastPrice(self, tikr):
        data = yf.Ticker(tikr).history(period='1d')
        return pd.to_numeric(data['Close'], errors='coerce')[0]

    def getAnnualRateOfGrowth(self, eps):
        lastEarnings = eps[0]
        # lastEarnings = self.getLastEarningPerShareCorrected(eps)
        firstEarnings = eps[10]
        return pow(lastEarnings/firstEarnings, 1.0/self.numYears)-1

    def getEpsValueTenYears(self, eps, annualRateOfGrowth):
        lastEarnings = eps[0]
        # lastEarnings = self.getLastEarningPerShareCorrected(eps)
        return lastEarnings * pow(1 + annualRateOfGrowth, self.numYears)
    
    def getMarketPriceTenYears(self, epsValueTenYears, pe):
        return epsValueTenYears * pe
    
    def getAnnualRateOfGrowthTenYears(self, marketPriceTenYears, currentPrice):
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
            data['annualRateOfGrowth'] = self.getAnnualRateOfGrowth(member['eps'])
            data['epsValueTenYears'] = self.getEpsValueTenYears(member['eps'], data['annualRateOfGrowth'])
            data['marketPriceTenYears'] = self.getMarketPriceTenYears(data['epsValueTenYears'], member['minPE10Years'])
            data['annualRateOfGrowthTenYears'] = self.getAnnualRateOfGrowthTenYears(data['marketPriceTenYears'], data['currentPrice'])

            result[count] = data.copy()
            count = count + 1
        return result
    
    def printEstimations(self, result):
            for data in result:
                if data['currency'] == "USD":
                    currencySymbol = "$"
                else:
                    currencySymbol = "€"
            
                print("-----------------------------------------------------------")
                print(data['name'] + " (" + data['tikr'] + "):")
                print("     Earnings per share have a annual rate of growth of " + str(round(data['annualRateOfGrowth'], 4)*100) + "%, ")
                print("     with this rate the earnings per share for ten years from now will be " + str(round(data['epsValueTenYears'], 2)) + currencySymbol + ". Multiplying this for the min PE of ")
                print("     last ten years we get a market price of " + str(round(data['marketPriceTenYears'], 2)) + currencySymbol + " per share to ten years. If the current price is " + str(round(data['currentPrice'], 2)) + currencySymbol )
                print("     whe could get a annual rate of growth of " + str(round(data['annualRateOfGrowthTenYears']*100, 2)) + "%.")

    def buildReportHTML(self):
        result = self.getStockEstimationsTenYears()
        now = datetime.now()
        report = ("<!DOCTYPE html>\n"
                 +"<html>\n"
                 +"      <body>\n"
                 +"         <h1 style="+ '"' + "color:SlateGray; font-family:Courier New, monospace;" '"' + ">Stock list report</h1>\n"
                 +"         <h3 style="+ '"' + "color:SlateGray; font-family:Courier New, monospace;" '"' + ">Date: " + now.strftime("%d/%m/%Y %H:%M:%S") + "</h3>\n")
        
        for data in result:
            url = self.getLogoImageUrl(data['tikr'])
            priceEarnings = self.getPriceEarnings(data['tikr'])

            if data['currency'] == "USD":
                currencySymbol = "$"
            else:
                currencySymbol = "€"
            if data['annualRateOfGrowthTenYears'] >= 0.06:
                colorClass = 'color: green'
            else:
                colorClass = 'color: red'

            report += (" <img src=" + '"' + url + '"' + ">\n"
                +"         <h2 style=" + '"' + "color:SlateGray; font-family:Courier New, monospace;" '"' + ">" + data['name'] + " (" + data['tikr'] + ")" + "</h2>\n"
                +"         <h3 style="+ '"' + "font-family:Courier New, monospace;" '"' + ">Earnings per share have a <span style='"'color: blue'"'>annual rate of growth (eps) of " + str(round(data['annualRateOfGrowth']*100, 2)) + "%</span>, \n"
                +"with this rate the earnings per share for ten years from now will be " + str(round(data['epsValueTenYears'], 2)) + currencySymbol + ". Multiplying this for the min PE of \n"
                +"last ten years (PE last 12 months: "+ priceEarnings +") we get a market price of " + str(round(data['marketPriceTenYears'], 2)) + currencySymbol + " per share to ten years. If the current price is " + str(round(data['currentPrice'], 2)) + currencySymbol + "\n"
                +"whe  <span style=" + '"' + colorClass + '"' + ">could get a annual rate of growth of " + str(round(data['annualRateOfGrowthTenYears']*100, 2)) + "%.</span></h3>\n")    
        report += ("      </body>\n"
                +"</html>")        
        # file = open("sample.html","w")
        # file.write(report)
        # file.close()
        return report         

    def sendEmail(self, contact, subject, htmlMessage):
        EMAIL_ADDRESS = os.environ.get('EMAIL_USER')
        EMAIL_PASSWORD = os.environ.get('EMAIL_PASS')

        msg = EmailMessage()
        msg['Subject'] = subject
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = contact

        msg.add_alternative(htmlMessage, subtype='html')

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)
        
    def sendAlert(self, report):
        self.sendEmail('sanchezmosquerajosemanuel@gmail.com', 'Stock list report', report)               

    def getLogoImageUrl(self, tikr):
        # data = yf.Ticker(tikr)
        # return data.info['logo_url']
        try:
            headers = {'User-agent': 'Mozilla/5.0'}
            url = ("https://finance.yahoo.com/quote/{}/profile?p={}".format(tikr,tikr))
            webpage = requests.get(url, headers=headers)
            soup = BeautifulSoup(webpage.content, 'html.parser')
        
            links = soup.findAll('p')
            lines = str(links).split('\n')
        
            domain = re.search('href="https://(.*?)"', lines[0]).group(1)
            imageUrl = 'https://logo.clearbit.com/%s' % domain.split('/')[0].replace('www.', '')
        except Exception:
            imageUrl = ''
            pass
        
        return imageUrl
        
    def getPriceEarnings(self, tikr):
        Event().wait(10)
        try:
            headers = {'User-agent': 'Mozilla/5.0'}
            url = ("https://es.finance.yahoo.com/quote/" + tikr + "/key-statistics") 
            webpage = requests.get(url, headers=headers)
            soup = BeautifulSoup(webpage.content, 'html.parser')
    
            links = soup.findAll('table')
            lines = str(links).split('\n')
    
            priceEarnings = re.findall(r'[\d]*[.][\d]+', lines[0])
        except Exception:
            return 'N/A'
            pass
        if len(priceEarnings) > 3:  
            return priceEarnings[2] # Position 2 is PE
        else:
            return 'N/A'