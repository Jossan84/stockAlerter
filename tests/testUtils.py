#testUtils.py
#06/09/2022

import sys

sys.path.append( '../utils' )

# Test getEarningsPerShare function
from getEarningsPerShare import getEarningsPerShare

tikr = 'BAMXF'
years, eps = getEarningsPerShare(tikr)
print(years, eps)

tikr = 'AAPL'
years, eps = getEarningsPerShare(tikr)
print(years, eps)