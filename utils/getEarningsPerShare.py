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
    
    if (len(soup) == 0):
        return [], []
    
    try:
        lines = str(links0).split('\n')
        eps = [float(re.search('\$(.*?)<',lines[2]).group(1))]
        year = [int(re.search(', (.*?) was',lines[2]).group(1))]
    except:
        eps = []
        year = []
                
    for link in range(0, 24, 2):
        year_ = int(re.search('>(.+?)<',str(links[link])).group(1))
        eps_ = float(re.search('>\$(.+?)<',str(links[link+1])).group(1))
        if year_ in year:
            index = year.index(year_)
            year[index] = year_
            eps[index] = eps_
        else:
            eps.append(eps_)
            year.append(year_)
    return year, eps
    
def getMinPriceEarnigsRatio(tikr):
    url = 'https://www.macrotrends.net/stocks/charts/' + tikr + '/apple/pe-ratio'
    page = requests.get(url) # Getting page HTML through request
    soup = BeautifulSoup(page.content, 'html.parser') # Parsing content using beautifulsoup

    # links = soup.findAll('td', style='text-align:center;')
    links = soup.findAll('tr')
    lines = str(links).split('\n')
    
    min = float('inf')
    for i in range(11, 250, 5):
        val = float(re.search('">(.+?)<',str(lines[i])).group(1))
        if val < min:
            min = val
        # print("Line " + str(i) + ": " + lines[i])
        # print(re.search('>(.+?)<',str(lines[i])).group(1))
    return min    
    