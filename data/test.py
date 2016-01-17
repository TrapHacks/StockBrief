import csv
import sys
with open('results.csv', 'rb') as readcsv:
    reader = csv.reader(readcsv)
    with open('columns.csv', 'w') as columnscsv:
        writer = csv.writer(columnscsv, delimiter=',')
        writer.writerow(['Date', 'Tweet', 'Sentiment'])
        for row in reader:
            if len(row) > 3:
                print 'broken'
                sys.exit()
            else:
                writer.writerow([row[0],row[1], row[2]])
        
