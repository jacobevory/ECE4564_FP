#!/usr/bin/env python3

from avkey.py import AVKEY

#Checkpoint: Initialize appropriate libraries, time, json, etc.
#Checkpoint: Read stock data from file and store in 2 dimensional array/vector/mapped-list wtf ever
#Checkpoint: Enter infinite loop
#Checkpoint: Reset global change variable
#Checkpoint: Make http request for each stock, store first set of data in array
#Checkpoint: Check close price against open price, calculate $$$ difference, add to global day change variable
#Checkpoint: Repeat for all stocks in list
#Checkpoint: Calculate PERCENTAGE change overall
#Checkpoint: Compare and store percentage change to pre-defined intervals
#Checkpoint: Set LED color to reflect percentage change
#				Red: 	change < -4%
#				Yellow:	-4% > change > 4%
#				Green:	4% > change
#			Potentially define gradient, the RGB ring is capable of anything.

import requests
import csv
import pprint

stockGainTot = 0

reader = csv.reader(open('stockinput.csv', 'r'))
symbols = {}
for line in reader:
    k, v = line
    symbols[k] = v

pprint.pprint(symbols)

for stock, boughtPrice in symbols.items():
    r = requests.get('https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=' + stock + '&apikey=' + key)
    d = r.json()
    series = d['Time Series (Daily)']
    timeData = next(iter(series))

    #get most recent close value
    stockData = series[timeData]
    closeVal = stockData['4. close']
    openVal = stockData['1. open']

    stockGain = (float(closeVal) - float(openVal))
    stockGainTot = stockGainTot + stockGain
    print('The close value for ' + stock + ' on '+ timeData + ' is ' + closeVal + ' (' + str(stockGain) + ')')

print('Overall stock gain: %.2f' % stockGainTot)