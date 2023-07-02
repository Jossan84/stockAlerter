# TestCorrectEarnings.py
# 30/06/2023

import json
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime


def estimateCoefficients(x, y):
    # Number of observations/points
    n = np.size(x)

    # Mean of x and y vector
    m_x = np.mean(x)
    m_y = np.mean(y)

    # Calculating cross-deviation and deviation about x
    SS_xy = np.sum(y * x) - n * m_y * m_x
    SS_xx = np.sum(x * x) - n * m_x * m_x

    # Calculating regression coefficients
    b1 = SS_xy / SS_xx
    b0 = m_y - b1 * m_x

    return b0, b1


def getLastEarningPerShareCorrected(eps):
    x = np.array(list(range(1, len(eps) + 1)))
    a = estimateCoefficients(x, eps)

    epsCorrected = a[0] + a[1] * x

    n = len(x) - 1
    return epsCorrected[n]


# Plot data
font = {'family': 'serif',
        'color': 'darkred',
        'weight': 'normal',
        'size': 16,
        }

# Get Data
with open('../../data/stocksData.json') as json_file:
    data = json.load(json_file)
values = data['members']

for value in values:
    # Get values
    years = list(map(str, value['years']))
    eps = value['eps']
    name = value['name']
    currency = value['currency']

    dateList = np.array(years)
    dataList = np.array(eps)

    # Sort data by date
    dates = []
    for date in dateList:
        dates.append(datetime.strptime(date, '%Y'))

    index = [sorted(dates).index(x) for x in dates]
    dates = np.array(dates)
    dates = dates[index]
    data = dataList[index]

    # Linear Estimation
    x = np.array(list(range(1, len(eps)+1)))
    y = data
    a = estimateCoefficients(x, y)

    # Prediction
    xPrediction = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23])
    yPrediction = np.array(["2010", "2011", "2012", "2013", "2014", "2015", "2016", "2017", "2018", "2019", "2020",
                            "2021", "2022", "2023", "2024", "2025", "2026", "2027", "2028", "2029", "2030", "2031",
                            "2032"]
                           )
    dataPredicted = a[0] + a[1] * xPrediction

    # Convert dates to datetime type
    datesPredicted = []
    for date in yPrediction:
        datesPredicted.append(datetime.strptime(date, '%Y'))

    # Plot data
    n = len(dates)-1
    plt.plot(dates, data, 'o-')
    plt.plot(datesPredicted, dataPredicted, 'r-')
    plt.plot(dates[n], data[n], 'ok')
    plt.plot(datesPredicted[datesPredicted.index(dates[n])], dataPredicted[datesPredicted.index(dates[n])], 'ok')
    plt.text(dates[n], data[n], data[n])
    plt.text(datesPredicted[datesPredicted.index(dates[n])], dataPredicted[datesPredicted.index(dates[n])],
             round(dataPredicted[datesPredicted.index(dates[n])], 2))
    plt.gcf().autofmt_xdate()
    plt.title(f"{name}", fontdict=font)
    plt.grid()
    plt.xlabel("Date", fontdict=font)
    plt.ylabel(f"Price [{currency}]", fontdict=font)
    plt.show()
