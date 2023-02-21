# testGetFinantialRatios.py
# 21/02/2023

#!pip install urllib3
#!pip install bs4

# For data manipulation
import pandas as pd
from urllib.request import urlopen, Request

# To extract fundamental data
from bs4 import BeautifulSoup

# Functions to Parse Data from FinViz
def fundamental_metric(soup, metric):
    return soup.find(text = metric).find_next(class_='snapshot-td2').text
    
def get_fundamental_data(df):
    for symbol in df.index:
        try:
            url = ("http://finviz.com/quote.ashx?t=" + symbol.lower())
            req = Request(url=url,headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:20.0) Gecko/20100101 Firefox/20.0'}) 
            response = urlopen(req)
            soup = BeautifulSoup(response, features='html.parser')
            for m in df.columns:                
                df.loc[symbol,m] = fundamental_metric(soup,m)                
        except Exception as e:
            print (symbol, 'not found')
    return df


# List of Stocks and Ratios You are Interested In    
stock_list = ['VEEV','AAPL','CPRT','IDXX','ODFL','SAIA','FOXF','TREX','NVDA','GOOGL','DSGX',
              'COST', 'NSSC', 'BMW.DE', 'LULU', 'MA', 'V', 'DHR', 'ADBE', 'MNST', 'MCO', 'VRSK',
              'AME', 'NVO', 'AWK', 'PSA', 'EXR', 'FNV', 'VRSN', 'ANET', 'MPWR', 'TSM', 'MSFT',
              'CHKP', 'EXPO']

metric = ['P/B',
'P/E',
'Forward P/E',
'PEG',
'Debt/Eq',
'EPS (ttm)',
'Dividend %',
'ROE',
'ROI',
'EPS Q/Q',
'Insider Own'
]

# Initialize Pandas DataFrame to Store the Data
df = pd.DataFrame(index=stock_list,columns=metric)
df = get_fundamental_data(df)
print(df)

# Data Clearning: Further Parse the Data into Numeric Types [Remove % Sign and Convert Values to Numeric Type]
df['Dividend %'] = df['Dividend %'].str.replace('%', '')
df['ROE'] = df['ROE'].str.replace('%', '')
df['ROI'] = df['ROI'].str.replace('%', '')
df['EPS Q/Q'] = df['EPS Q/Q'].str.replace('%', '')
df['Insider Own'] = df['Insider Own'].str.replace('%', '')
df = df.apply(pd.to_numeric, errors='coerce')
print(df)

# Filter Good Companies
# Companies which are quoted at low valuations [P/E < 15 and P/B < 1]
df_filtered = df[(df['P/E'].astype(float)<15) & (df['P/B'].astype(float) < 1)]
print(df_filtered)

# Further filter companies which have demonstrated earning power [EPS Q/Q > 10%]
df_filtered = df_filtered[df_filtered['EPS Q/Q'].astype(float) > 10]
print(df_filtered)

# Management having substantial ownership in the business [Insider Own > 30%]
df = df[df['Insider Own'].astype(float) > 30]
print(df)