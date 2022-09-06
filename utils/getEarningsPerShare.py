#getEarningsPerShare.py
#06/09/2022

import re
import requests
from bs4 import BeautifulSoup

def getEarningsPerShare(tikr):
    
    url = 'https://www.macrotrends.net/stocks/charts/' + tikr + '/apple/eps-earnings-per-share-diluted'
    page = requests.get(url) # Getting page HTML through request
    soup = BeautifulSoup(page.content, 'html.parser') # Parsing content using beautifulsoup

    # links = soup.findAll('table', class_='historical_data_table')
    links0 = soup.findAll('ul', style='margin-top:10px;')
    links = soup.findAll('td', style='text-align:center')


    try:
        lines = str(links0).split('\n')
        eps = [float(re.search('\$(.*?)<',lines[2]).group(1))]
        year = [int(re.search(', (.*?) was',lines[2]).group(1))]
    except:
        eps = []
        year = []
    
    for link in range(22):
        if(link % 2):
            epsValue = float(re.search('\$(.+?)<',str(links[link])).group(1))
            eps.append(epsValue)
        else:
            yearValue = int(re.search('>(.+?)<',str(links[link])).group(1)) 
            year.append(yearValue)
    return year, eps