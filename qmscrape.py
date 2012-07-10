#!/usr/bin/env python

'''
Caution: This scraper only returns dividend adjusted closing prices and cannot
be expected to agree with the others
'''

import urllib2
import csv
from scraperutil import *

def gethistory(symbol):
    _atonce = 300
    end = endtime()
    start = end - datetime.timedelta(_atonce)

    urltemplate = 'http://app.quotemedia.com/quotetools/getHistoryDownload.csv?&webmasterId=501&startDay={startday}&startMonth={startmonth}&startYear={startyear}&endDay={endday}&endMonth={endmonth}&endYear={endyear}&isRanged=false&symbol={symbol}'

    fulllist = []
    dates = set()

    while True:
        url = urltemplate.format(symbol=symbol,
                                 endday=end.day,
                                 endmonth=end.month,
                                 endyear=end.year,
                                 startday=start.day,
                                 startmonth=start.month,
                                 startyear=start.year)

        alldupe = True
        for line in csv.DictReader(urllib2.urlopen(url)):
            date = line['date']
            if date not in dates:
                alldupe = False
                dates.add(date)
                newline = {}
                try:
                    date = formatdate(line['date'], '%Y-%m-%d')
                except ValueError:
                    continue
                newline['Date'] = date
                newline['Open'] = round(float(line['open']), 2)
                newline['Close'] = round(float(line['close']), 2)

                fulllist.append(newline)
        if alldupe:
            break
        (start, end) = (start - datetime.timedelta(_atonce), start)

    return fulllist

if __name__ == "__main__":
    import sys
    printdata(gethistory(sys.argv[1]))
