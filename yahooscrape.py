#!/usr/bin/env python

import urllib2
import csv
from scraperutil import *

def gethistory(symbol):
    yesterday = endtime()

    req = 'http://ichart.finance.yahoo.com/x?s={0}&d={1}&e={2}&f={3}&z=30000'.format(
        symbol, yesterday.month - 1, yesterday.day, yesterday.year)

    ratios = {}
    fulllist = []
    for line in csv.reader(urllib2.urlopen(req)):
        if line[0] == 'SPLIT':
            date = line[1].strip()
            ratio = line[2]
            (denom, num) = ratio.split(':')
            ratios[date] = float(num) / float(denom)
        else:
            date = line[0].strip()
            newline = {}
            try:
                newline['Date'] = formatdate(date, '%Y%m%d')
            except ValueError:
                continue
            newline['Open'] = float(line[1])
            newline['Close'] = float(line[4])
            for d in ratios:
                if d > date:
                    newline['Open'] *= ratios[d]
                    newline['Close'] *= ratios[d]

            newline['Open'] = round(newline['Open'], 2)
            newline['Close'] = round(newline['Close'], 2)
            fulllist.append(newline)

    return fulllist

if __name__ == "__main__":
    import sys
    printdata(gethistory(sys.argv[1]))
