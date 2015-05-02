import csv
import sys
import json
import pymongo
from bson.objectid import ObjectId

rows = []
output = {}

# Get Complaint Type from: https://nycopendata.socrata.com/Social-Services/311-Complaint-Types/h4xh-jcuz
# https://nycopendata.socrata.com/Social-Services/311-Service-Requests-from-2010-to-Present/erm2-nwe9
complaint_type = ["Air Quality",
		"Building/Use", #Illegal Use of the Unit
		"Electrical", #Electrical Wiring Defective Exposed
		"Noise",
		"Rodent",
		"Sewer",
		"Sanitation",
		"Street Condition",
		"Water System"]

def setup_db():
    mongoUri = 'mongodb://zhou:cu6998@ds061711.mongolab.com:61711/survisor'
    client = pymongo.MongoClient(mongoUri)
    db = client.get_default_database()
    db311 = db['db311']
    return db311

def parse_complaint(row):
    for ct in complaint_type:
        if ((row['Complaint Type'].find(ct) != -1) and (row['Borough'] == "MANHATTAN")):
            rows.append(row)
            return

def parse_311_csv():
    f = open(sys.argv[1], 'rt')
    db = setup_db()
    try:
        reader = csv.DictReader(f)
        for row in reader:
	    parse_complaint(row)

    finally:
        f.close()
        for row in rows:
            output = {}
            output['type'] = row['Complaint Type'];
            output['zip'] = row['Incident Zip']
            output['addr'] = row['Incident Address']
            output['lat'] = row['Latitude']
            output['long'] = row['Longitude']
            db.insert(output)
            #output.append((row['Complaint Type'], row['Incident Zip'], row['Incident Address'], row['Latitude'], row['Longitude']))


