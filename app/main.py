#main.py
#24/08/2022

import os
import time
from stockAlerter import StockAlerter

def main():

    startTime = time.time()

    rootDir = os.path.dirname(os.path.realpath(__file__)).replace('\\app','').replace('/app','')
    dataFilePath = (rootDir + "\data\stocksData.json").replace('\\', '/')

    stockAlerter = StockAlerter(dataFilePath)
    result = stockAlerter.getStockEstimationsTenYears()
    report = stockAlerter.buildReportHTML()
    stockAlerter.sendAlert(report)

    endTime = time.time()
    elapsedTime = round(endTime - startTime, 2)
    print('Elapsed time: ', elapsedTime, ' seconds') 

if __name__ == "__main__":
    main()