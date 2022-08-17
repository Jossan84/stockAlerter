#TestYahooFinance.py
#16/08/2022

import yfinance as yf
# Request historical data for past 5 years
data = yf.Ticker("CPRT").history(period='1d')
# Show info
print(data['Close'])