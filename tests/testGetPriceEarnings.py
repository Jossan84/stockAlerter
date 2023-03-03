# testGetPriceEarnings.py
# 21/02/2023

#!pip install urllib3
#!pip install bs4

# For data manipulation
import re
import requests

# To extract fundamental data
from bs4 import BeautifulSoup
    
def getPriceEarnings(tikr):
    try:
        headers = {'User-agent': 'Mozilla/5.0'}
        url = ("https://es.finance.yahoo.com/quote/" + tikr + "/key-statistics") 
        webpage = requests.get(url, headers=headers)
        soup = BeautifulSoup(webpage.content, 'html.parser')
   
        links = soup.findAll('table')
        lines = str(links).split('\n')
  
        priceEarnings = re.findall(r'[\d]*[.][\d]+', lines[0])
    
    except Exception:
        priceEarnings = 'N/A'
        pass
        
    return priceEarnings[2] # Position 2 is PE

priceEarnings = getPriceEarnings('TSM')
print(priceEarnings)
priceEarnings = getPriceEarnings('QLYS')
print(priceEarnings)