#!/usr/bin/env python

import sys
import googlescrape as google
import yahooscrape as yahoo
import fcscrape as financialcontent
import scraperutil
from collections import defaultdict
from itertools import combinations

def approxeq(a, b, tol=0.015):
    return abs(a - b) <= tol

def majority(a, b, c):
    for k, l in combinations([a, b, c], 2):
        if None is not k and None is not l and approxeq(k, l):
            return k
    return None

def accuracy(name, compare, base):
    cdates = set(line['Date'] for line in compare)
    bdates = set(line['Date'] for line in base)
    bonly = bdates - cdates
    conly = cdates - bdates

    commondates = bdates & cdates
    compdata = {}
    for line in compare:
        compdata[line['Date']] = line

    agree = 0
    total = 0.0000000000000001
    for line in base:
        if line['Date'] not in commondates:
            continue
        if approxeq(line['Close'], compdata[line['Date']]['Close']):
            agree += 1
        total += 1

    print name.upper(),
    print 'missing', len(bonly), 'days,',
    print 'inserted', len(conly), 'days,',
    print 'agreed on {0}/{1} days. ({2}%)'.format(agree,
                                                  total,
                                                  agree/float(total))

symbol = sys.argv[1]
datasources = [
    ('google', google.gethistory(symbol)),
    ('yahoo', yahoo.gethistory(symbol)),
    ('financialcontent', financialcontent.gethistory(symbol))
    ]

unified = defaultdict(lambda: defaultdict(dict))
for dsname, ds in datasources:
    for line in ds:
        unified[line['Date']][dsname]['Close'] = line['Close']

best_guess = []
for date in sorted(unified, reverse=True):
    day = unified[date]
    winner = majority(
        day['google'].get('Close', None),
        day['yahoo'].get('Close', None),
        day['financialcontent'].get('Close', None))

    if winner:
        best = {}
        best['Date'] = date
        best['Close'] = winner
        best_guess.append(best)

for dsname, ds in datasources:
    accuracy(dsname, ds, best_guess)

scraperutil.printdata(best_guess)
