#getEarningsData.py
#11/09/2022

import json
import yfinance as yf
from getEarningsPerShare import getEarningsPerShare
from getEarningsPerShare import getMinPriceEarnigsRatio


data = {"stocksList": "List of stocks to track",
        "members": []
       }

member={"name": "",
        "tikr": "",
        "currency": "",
        "minPE10Years": [],
        "years": [],
        "eps": []
       }

stockList = ['VEEV', 'AAPL', 'CPRT', 'IDXX', 'ODFL', 'SAIA', 'FOXF', 'POOL', 'LEN', 'NSSC',
             'MTH', 'TREX', 'ORLY', 'BOOT', 'MBUU', 'CUBE', 'NVDA', 'GOOGL', 'DSGX','QLYS',
             'LULU']

members = []
for k in range(len(stockList)):
    tikr = stockList[k]
    data_= yf.Ticker(tikr)
    years, eps = getEarningsPerShare(tikr)
    minPE10Years = getMinPriceEarnigsRatio(tikr)
    member["name"] = data_.info["shortName"]
    member["tikr"] = stockList[k]
    member["currency"] = data_.info["currency"]
    member["minPE10Years"] = max(minPE10Years, 15)
    member["years"] = years
    member["eps"] = eps
    members.append(member.copy())

data["members"] = members

# Export data
with open("sample.json", "w") as outfile:
    json.dump(data, outfile)

# Print data
json_object = json.dumps(data, indent = 4) 
print(json_object)