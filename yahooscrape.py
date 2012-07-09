#!/usr/bin/env python

import urllib2
import sys
import csv
import datetime
from scraperutil import *

yesterday = endtime()
symbol = sys.argv[1]

req = 'http://ichart.finance.yahoo.com/table.csv?s={0}&d={1}&e={2}&f={3}'.format(
    symbol, yesterday.month - 1, yesterday.day, yesterday.year)

fulllist = []
for line in csv.DictReader(urllib2.urlopen(req)):
    line['Date'] = formatdate(line['Date'], '%Y-%m-%d')
    fulllist.append(line)

printdata(fulllist)
