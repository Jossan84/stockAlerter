#importData.py
#17/08/2022

import json

def importData(fileName):
    with open(fileName) as json_file:
        data = json.load(json_file)    
    return data

def printData(data):  
    # Print the data of dictionary
    for i in data['members']:
        print("Name:", i['name'])
        print("Tikr:", i['tikr'])
        print("Currency:", i['currency'])
        print("PE:", i['minPE10Years'])
        print("Years:", i['years'])
        print("EPS:", i['eps'])
        print()