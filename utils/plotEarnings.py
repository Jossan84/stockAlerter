#plotEarnings.py
#11/09/2022

import matplotlib.pyplot as plt
# from getEarningsPerShare import getEarningsPerShare

tikr = 'AAPL'
# years, eps = getEarningsPerShare(tikr)

years =  [ 2022, 2021, 2020, 2019, 2018, 2017, 2016, 2015, 2014, 2013, 2012, 2011 ]
eps = [ 2.63, 2.36, 1.90, 1.47, 0.98, 0.53, 0.38, 0.28, 0.15, 0.11, 0.02, 0.02 ]

plt.title('Earnings per Share ' + tikr)
plt.plot(years, eps, 'b.-')
plt.xlabel('Years')
plt.ylabel('EPS [$]')
plt.grid(True)
plt.show()