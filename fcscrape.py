#!/usr/bin/env python

import urllib2
import sys
import datetime
import time
import csv
from scraperutil import *

yesterday = datetime.datetime.now() - datetime.timedelta(1)
year = yesterday.year

urltemplate = "http://markets.chron.com/chron/?Method=gethistoricalcsv&Month={month}&Page=HISTORICAL&Year={year}&Range=12&Ticker={symbol}"

fulllist = []
dates = set()

for y in range(year, 1900, -1):
    url = urltemplate.format(symbol=sys.argv[1],
                             month=12,
                             year=y)
    empty = True
    for line in csv.DictReader(urllib2.urlopen(url)):
        empty = False
        line['Date'] = formatdate(line['Date'], '%m/%d/%y')
        fulllist.append(line)
    if empty:
        break

printdata(fulllist)
