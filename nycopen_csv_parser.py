import csv
import sys
import json

rows = []
output = []

f = open(sys.argv[1], 'rt')
try:
    reader = csv.DictReader(f)
    for row in reader:
	if row['Complaint Type'].find("Complaint"):
        	rows.append(row)
finally:
    f.close()
    #print json.dumps(rows)
    for row in rows:
        output.append((row['Complaint Type'], row['City'], row['Incident Address']))
    print output
