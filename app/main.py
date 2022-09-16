#main.py
#24/08/2022

import os
from stockAlerter import StockAlerter

def main():
    rootDir = os.path.dirname(os.path.realpath(__file__)).replace('\\app','').replace('/app','')
    dataFilePath = (rootDir + "\data\stocksData.json").replace('\\', '/')

    stockAlerter = StockAlerter(dataFilePath)
    result = stockAlerter.getStockEstimationsTenYears()
    report = stockAlerter.buildReportHTML()
    stockAlerter.sendAlert(report)

if __name__ == "__main__":
    main()