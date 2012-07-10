#!/usr/bin/env python

import urllib2
import sys
import datetime
import time
import csv
from scraperutil import *

def gethistory(symbol):
    end = endtime()
    year = end.year

    urltemplate = "http://markets.chron.com/chron/?Method=gethistoricalcsv&Month={month}&Page=HISTORICAL&Year={year}&Range=12&Ticker={symbol}"

    # Pull split data from yahoo to adjust
    splitreq = 'http://ichart.finance.yahoo.com/x?s={0}&d={1}&e={2}&f={3}&z=30000'.format(
        symbol, end.month - 1, end.day, end.year)

    ratios = {}
    for line in csv.reader(urllib2.urlopen(splitreq)):
        if line[0] == 'SPLIT':
            date = line[1].strip()
            try:
                date = formatdate(date, '%Y%m%d')
            except ValueError:
                continue
            ratio = line[2]
            (denom, num) = ratio.split(':')
            ratios[date] = float(num) / float(denom)

    fulllist = []
    dates = set()

    for y in range(year, 1900, -1):
        url = urltemplate.format(symbol=symbol,
                                 month=12,
                                 year=y)
        empty = True
        for line in csv.DictReader(urllib2.urlopen(url)):
            empty = False
            line['Date'] = formatdate(line['Date'], '%m/%d/%y')

            line['Open'] = float(line['Open'])
            line['Close'] = float(line['Close'])
            for d in ratios:
                if d > line['Date']:
                    line['Open'] *= ratios[d]
                    line['Close'] *= ratios[d]

            line['Open'] = round(line['Open'], 2)
            line['Close'] = round(line['Close'], 2)

            fulllist.append(line)
        if empty:
            break

    return fulllist

if __name__ == "__main__":
    import sys
    printdata(gethistory(sys.argv[1]))
