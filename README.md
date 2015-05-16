# Survisor

## Data source

### AirBnB

Data is collected by self-written crawler. Each month the price listings of all New York region are crawled. For a specific date, duration of stay ranging from 1 day to 7 days are collected. All records are pushed to MongoDB. 

Here is one sample record from collection "ablist": 

```
{
    "_id": {
        "$oid": "5545195dca1a2c041d3855e2"
    },
    "data-url": "/rooms/6194193?checkin=5%2F2%2F2015&checkout=5%2F9%2F2015&s=GH-A",
    "data-lat": "40.815913034028426",
    "data-price": "<sup>$<\/sup>100<sup><\/sup>",
    "data-id": "6194193",
    "class": [
        "listing"
    ],
    "data-name": "King sized bedroom in a 2bed apt",
    "itemscope": "",
    "data-user": "18891247",
    "data-lng": "-73.95168153902351",
    "itemtype": "http://schema.org/Enumeration"
}
```

Requirement to use the package: PyMongo, BeautifulSoup4, lxml parser, Python3. 

### Yelp

Collection name:

    yelpDB

Total record number:

    201950

Column name:

    _id
    name
    rating
    latitude
    longitude
    zip

One record example:

```
    { "_id" : ObjectId("55469ad5300446310dd2c3c3"), 
      "name" : "Cookshop", 
      "rating" : 4, 
      "latitude" : 40.7454262, 
      "longitude" : -74.0056076, 
      "zip" : 10001 }
```


NOTES:
Required lib to run the program:
    json_simple-1.1.jar
    scribe-1.3.5.jar
    mongo-java-driver-2.11.3.jar

### NYC311

Many kinds of complain data are collected. 

```
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
```

Here is a sample record. 

```
{
    "_id": {
        "$oid": "554515181d41c86c75a1fe9d"
    },
    "addr": "19 EAST 127 STREET",
    "zip": "10035",
    "long": "-73.94056006628847",
    "lat": "40.807404902674044",
    "type": "Noise - Street/Sidewalk"
}
```

### Flask Server
Launch AirBnB_Crawler/server.py as the server to serve request for the APP:

A simple command to try it out would be **curl -H Content-type: application/json -X POST http://127.0.0.1:5000/messages -d '{"id":"246030", "yr":"2015", "month":"05", "day":"16", "duration":"1"}'**

The above command can tell the server to crawl the page that contains detail data of a listing.

If you want to try to launch the server and play with it, all you need is to change the IP to the address where the server is hosted on. The server accepts input data in JSON format as what's written after  **-d**. You need to sepcify the "data-id", "movein yy, mm, dd" and also the duration of the stay.

Here's a sample json out generated from the query command above:

{"photo": "https://a2.muscache.com/ic/pictures/79522229/7d8647fc_original.jpg?interpolation=lanczos-none&size=x_large&output-format=progressive-jpeg&output-quality=70", "desc": "Apartment in New York, United States. The Space I&#x27;m renting 2 rooms in a 3 bedrooms apartment.  The price you see is the price for 1 room (2 ppl) If you want to book both rooms (capacity 4ppl total) you would need to go on both listings below:  https://www.airbnb.com/rooms/244547  htt...", "neighborhood": "UpperEastSide", "price": "$89", "rating": "4.5"}

It currently crawls the photo link, description, price, rating and the neighborhood of a specific listing!
