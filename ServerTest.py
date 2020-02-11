"""import csv
r = csv.reader(open('stock.csv', ),delimiter=";")
lines = list(r)
lines[0][1] = "sondre"
writer = csv.writer(open('stock.csv', 'w', newline="" ),delimiter=";")

"""

import csv
r = csv.reader(open('stock.csv', ),delimiter=";")
lines = list(r)
lines[0][2]= "abc"
writer = csv.writer(open('stock.csv', 'w', newline="" ),delimiter=";")

"""for line_number in range(len(lines)):
    x = lines[line_number]
    if x[0] == '1':
        x[2] = 5
    print(lines[line_number])
"""
writer.writerows(lines)
