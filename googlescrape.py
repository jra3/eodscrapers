#!/usr/bin/env python

import urllib2
import sys
import csv
import datetime
from scraperutil import *

_atonce = 300
end = endtime()
start = end - datetime.timedelta(_atonce)

urltemplate = 'http://www.google.com/finance/historical?q={symbol}&output=csv&startdate={start}&enddate={end}'
datekey = '\xef\xbb\xbfDate' # WTF google?

fulllist = []
dates = set()

while True:
    url = urltemplate.format(symbol=sys.argv[1],
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
            fulllist.append(line)

    if alldupe:
        break
    (start, end) = (start - datetime.timedelta(_atonce), start)

printdata(fulllist)
