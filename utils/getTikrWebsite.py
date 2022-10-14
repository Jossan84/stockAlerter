#getTikrWebsite.py
#13/10/2022

import re
import requests
from bs4 import BeautifulSoup

def getTikrWebsite(tikr):
    headers = {'User-agent': 'Mozilla/5.0'}
    url = ("https://finance.yahoo.com/quote/{}/profile?p={}".format(tikr,tikr))
    webpage = requests.get(url, headers=headers)
    soup = BeautifulSoup(webpage.content, 'html.parser')
    
    links = soup.findAll('p')
    lines = str(links).split('\n')
    # print(lines)
    domain = re.search('href="https://(.*?)"', lines[0]).group(1)
    
    logoUrl = 'https://logo.clearbit.com/%s' % domain.split('/')[0].replace('www.', '')#.replace('usa.', '')
    
    print(logoUrl)
   
getTikrWebsite('AAPL')   