import time
import datetime

order = ['Date', 'Open', 'Close', ]

def endtime():
    return datetime.datetime.now()# - datetime.timedelta(1)

def formatdate(datestr, informat):
    t = time.strptime(datestr, informat)
    if t.tm_year > 2030:  # incorrect interpretation of 2 digit date
        t.tm_year -= 100
    return time.strftime("%Y-%m-%d", t)

def printdata(rows):
    csvrows = [','.join([row[k] for k in order]) for row in rows]
    csvrows = list(set(csvrows)) # wtf duplicate rows
    csvrows.sort(reverse=True)
    print ','.join(order)
    for row in csvrows:
        print row
