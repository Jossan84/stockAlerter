#main.py
#24/08/2022

from stockAlerter import StockAlerter

def main():
    stockAlerter = StockAlerter('../data/stocksData.json')
    result = stockAlerter.getStockEstimationsTenYears()
    report = stockAlerter.buildReportHTML()
    stockAlerter.sendAlert(report)

if __name__ == "__main__":
    main()