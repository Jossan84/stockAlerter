#exportPlotEarnings.py
#11/09/2022

import os
import shutil
import matplotlib.pyplot as plt
from getEarningsPerShare import getEarningsPerShare

stockList = ['AAPL', 'MSFT', 'GOOG', 'META', 'NVDA', 'TMO', 'DHR', 'AMT', 'GS', 'AMAT',
             'REGN', 'LRCX', 'SNPS', 'KLAC', 'ORLY', 'LULU', 'FTNT', 'MSCI',
             'STM', 'IDXX', 'ODFL', 'TROW', 'VEEV', 'CPRT', 'DHI', 'SIVB', 'RJF',
             'LEN', 'URI', 'MPWR', 'ENTG', 'GNRC', 'TRU', 'POOL',
             'DPZ', 'RGEN', 'CE', 'RS', 'FNF', 'SBNY', 'CRL', 'CUBE', 'PHM', 
             'BLDR', 'DKS', 'WAL', 'NXST', 'CACC', 'SF', 'QLYS', 'DSGX', 'SFST', 'HBCP', 'UNTY',
             'TREX', 'SAIA', 'TOL', 'TRNO', 'ESNT', 'WNS', 'FOXF', 'SSD', 'EVR', 'NVR', 'PKBK', 
             'SKY', 'OTTR', 'MTH', 'CORT', 'APAM', 'MDC', 'BOOT', 'CVCO', 'MHO', 'MCRI', 'NSSC',
             'MBUU', 'KRNY', 'CCBG', 'SMBC', 'GCBC', 'PLBC', 'FCCO', 'PBHC', 'UBCP', 'UBOH']

imagesDir = 'plots'

if os.path.isdir(imagesDir):
    shutil.rmtree(imagesDir)
    os.mkdir(imagesDir)


for tikr in stockList:
    years, eps = getEarningsPerShare(tikr)

    f = plt.figure()
    plt.title('Earnings per Share ' + tikr)
    plt.plot(years, eps, 'b.-')
    plt.xlabel('Years')
    plt.ylabel('EPS [$]')
    plt.grid(True)
    f.savefig(imagesDir + "\\" + tikr +  ".png", bbox_inches='tight')
    plt.close()