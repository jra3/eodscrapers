#!/usr/bin/env python

import urllib2
import csv
import datetime
from scraperutil import *

def gethistory(symbol):
    _atonce = 300
    end = endtime()
    start = end - datetime.timedelta(_atonce)

    urltemplate = 'http://www.google.com/finance/historical?q={symbol}&output=csv&startdate={start}&enddate={end}'
    datekey = '\xef\xbb\xbfDate' # WTF google?

    fulllist = []
    dates = set()

    while True:
        url = urltemplate.format(symbol=symbol,
                                 start=start.strftime('%b+%d%%2C+%Y'),
                                 end=end.strftime('%b+%d%%2C+%Y'))

        alldupe = True # google returns default results if we go out of range, halt on seeing default data
        for line in csv.DictReader(urllib2.urlopen(url)):
            date = line[datekey]
            del line[datekey]
            if date not in dates:
                alldupe = False
                dates.add(date)
                line['Date'] = formatdate(date, '%d-%b-%y')
                line['Open'] = round(float(line['Open']), 2)
                line['Close'] = round(float(line['Close']), 2)
                fulllist.append(line)

        if alldupe:
            break
        (start, end) = (start - datetime.timedelta(_atonce), start)

    return fulllist

if __name__ == "__main__":
    import sys
    printdata(gethistory(sys.argv[1]))
