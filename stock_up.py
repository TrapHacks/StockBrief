#!/usr/bin/env python

import yahoo_finance
import csv
import time

with open('stocks.csv', 'rb') as stockfile:
    csv_reader = csv.reader(stockfile, delimiter=',', quotechar='|')
    next(csv_reader, None)
    
    for row in csv_reader:
        print '\n##########'
        print 'Stock:', row[1], '(' + row[0] + ')'
        
        stock = yahoo_finance.Share(row[0])
        stock_data = stock.get_historical('2000-01-01', '2015-12-31')

        print 'Got historical data'

        with open(stock.symbol + '.csv', 'wb') as outfile:
            if len(stock_data) > 0:
                print 'Writing to file'
                writer = csv.writer(outfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
                writer.writerow(stock_data[0].keys())

                count = 0
                for row in stock_data:
                    writer.writerow(row.values())
                    count += 1
                print 'Wrote', count, 'rows of data'
            else:
                print 'No data for stock:', stock.symbol

        time.sleep(0.2)
