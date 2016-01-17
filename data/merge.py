import csv
import os


symbol_map = {}

with open('constituents.csv', 'r') as readfile:
    reader = csv.reader(readfile)
    for row in reader:
        symbol_map[row[1].replace(' ', '_')] = row[0]


oc_map = {}

for key in symbol_map:
    try:
        with open(symbol_map[key] + '.csv') as csv_file:
            reader = csv.reader(csv_file)
            for row in reader:
                symbol = row[1]
                if symbol not in oc_map:
                    oc_map[symbol] = {}
                close = row[6]
                open_price = row[7]
                oc_map[symbol][row[5]] = (row[7], row[6])
    except:
        pass


date_dictionary = {}
# close = 6 open = 7
with open('results.csv', 'r') as readfile:
    reader = csv.reader(readfile)
    with open('ultra_results.csv', 'w') as outfile:
        writer = csv.writer(outfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
            for row in reader:
            try:
                date = row[0][:10]
                company_name = row[4]
                symbol = symbol_map[company_name]
                open_price = oc_map[symbol][date][0]
                close_price = oc_map[symbol][date][1]
                tweet = row[1]
            except:
                pass



    

