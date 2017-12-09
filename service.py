
#!/usr/bin/env python3

#Checkpoint: Initialize appropriate libraries, time, json, etc.
from avkey import AVKEY
import json
import requests
import csv
import smtplib
import pprint
import datetime
from neopixel import *
import argparse
import signal
import sys

def colorWipe(strip, color, wait_ms=50):
	 for i in range(strip.numPixels()):
                        strip.setPixelColor(i, Color(0, 0, 0))
                        strip.show()

def signal_handler(signal, frame):
		colorWipe(strip, Color(0,0,0))
		sys.exit(0)

def opt_parse():
		parser = argparse.ArgumentParser()
		parser.add_argument('-c', action='store_true', help='clear the display on exit')
		args = parser.parse_args()
		if args.c:
				signal.signal(signal.SIGINT, signal_handler)
lastLowerSent = 0
lastUpperSent = 0
totalPercentageChange = 0
upperLimit = 1
lowerLimit = 1

# LED strip configuration:
LED_COUNT	  = 12	  # Number of LED pixels.
LED_PIN		= 18	  # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN		= 10	  # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ	= 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA		= 5	   # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 255	 # Set to 0 for darkest and 255 for brightest
LED_INVERT	 = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL	= 0	   # set to '1' for GPIOs 13, 19, 41, 45 or 53
LED_STRIP	  = ws.WS2811_STRIP_GRB   # Strip type and colour ordering

# Create NeoPixel object with appropriate configuration.
strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, LED_STRIP)
# Intialize the library (must be called once before other functions).
strip.begin()

def setLED():
	if totalPercentageChange >= upperLimit :
		 for i in range(strip.numPixels()):
                        strip.setPixelColor(i, Color(0, 150, 0))
                        strip.show()
	elif totalPercentageChange <= -1*lowerLimit :
		 for i in range(strip.numPixels()):
                        strip.setPixelColor(i, Color(150, 0, 0))
                        strip.show()
	else :
		 for i in range(strip.numPixels()):
                        strip.setPixelColor(i, Color(0, 0, 150))
                        strip.show()
	return

setLED()
SMSgreeting = 'Hello! Thank you for signing up for the Peaceful Portfolio Notification System. You will be notified if your portfolio changes more than 4%.'
SMSlower = 'Your portfolio has decreased by more than ' + str(lowerLimit) + '%.'
SMSupper = 'Your portfolio has increased by more than ' + str(upperLimit) + '%.'
SMSsendFrom = 'peacefulportfolio'
SMSaddress = '7576331950@vtext.com'
seriesType = 'Time Series (1min)'

#Checkpoint: initialize smtp server and TLS connection
SMTPserver = smtplib.SMTP("smtp.gmail.com", 587)
SMTPserver.starttls()
SMTPserver.login('peacefulportfolio', 'PPPPPPPP')
SMTPserver.sendmail(SMSsendFrom, SMSaddress, SMSgreeting)

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
while True:
	opt_parse()
	#Checkpoint: Reset global change variable
	totalDollarChange = 0
	totalDollarOpen = 0
	totalPercentageChange = 0
	currentDay = now.day
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
	if (totalPercentageChange < (-1*lowerLimit)) and (lastLowerSent != currentDay):
		SMTPserver.sendmail(SMSsendFrom, SMSaddress, SMSlower)
		lastLowerSent = now.day
	if (totalPercentageChange > upperLimit) and (lastUpperSent != currentDay):
		SMTPserver.sendmail(SMSsendFrom, SMSaddress, SMSupper)
		lastUpperSent = now.day
	setLED()
