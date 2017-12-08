#!/usr/bin/env python3

#Checkpoint: Initialize appropriate libraries, time, json, etc.
from avkey import AVKEY
import json
import requests
import csv
import smtplib
import pprint

SMSgreeting = 'Hello! Thank you for signing up for the Peaceful Portfolio Notification System. You will be notified if your portfolio changes more than 4%.'
SMSaddress = '7576331950@vtext.com'
seriesType = 'Time Series (1min)'
#Checkpoint: initialize smtp server and TLS connection
SMTPserver = smtplib.SMTP("smtp.gmail.com", 587)
SMTPserver.starttls()
SMTPserver.login('peacefulportfolio', 'PPPPPPPP')
#SMTPserver.sendmail('peacefulportfolio@gmail.com', SMSaddress, SMSgreeting)

#imported 2 dimensional wtf ever: inputdata
stockSymbol = "NULL"
stockRequestURL = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=" + stockSymbol + "&outputsize=compact&apikey=" + AVKEY

#Checkpoint: Read stock data from file and store in 2 dimensional array/vector/mapped-list wtf ever
reader = csv.reader(open('stockinput.csv', 'r'))
symbols = {}
for line in reader:
	k, v = line
	symbols[k] = v

pprint.pprint(symbols)
#Checkpoint: Enter infinite loop
k = 1
while k == 1:
	k+=1
	#Checkpoint: Reset global change variable
	totalDollarChange = 0
	totalDollarOpen = 0
	totalPercentageChange = 0
	#Checkpoint: Make http request for each stock, store first set of data in array
	#Checkpoint: Check close price against open price, calculate $$$ difference, add to global day change variable
	#Checkpoint: Repeat for all stocks in list
	for stockSymbol, stockQuantity in symbols.items():
		stockRequestURL = "https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=" + stockSymbol + "&interval=1min&outputsize=compact&apikey=" + AVKEY
		r = requests.get(stockRequestURL)
		d = r.json()
		series = d[seriesType]
		timeData = next(iter(series))

		#get most recent close value
		stockData = series[timeData]
		closeVal = stockData['4. close']
		openVal = stockData['1. open']
		totalDollarOpen = (totalDollarOpen + float(openVal))
		stockGain = (float(closeVal) - float(openVal))
		totalDollarChange = totalDollarChange + stockGain
		print('The close value for ' + stockSymbol + ' on '+ timeData + ' is ' + closeVal + ' (' + str(stockGain) + ')')


#Checkpoint: Calculate PERCENTAGE change overall
	totalPercentageChange = ((totalDollarChange / totalDollarOpen) * 100)
	print(totalPercentageChange)

#Checkpoint: Compare and store percentage change to pre-defined intervals
#Checkpoint: Set LED color to reflect percentage change
#				Red:	 change < -4%
#				Yellow:	-4% > change > 4%
#				Green:	4% > change
#			Potentially define gradient, the RGB ring is capable of anything.
