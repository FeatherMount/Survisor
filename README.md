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

A simple command to try it out would be 
```
curl -H "Content-type: application/json" -X POST http://127.0.0.1:5000/messages -d '{"id":"246030", "yr":"2015", "month":"05", "day":"16", "duration":"1"}'
```

The above command can tell the server to crawl the page that contains detail data of a listing.

If you want to try to launch the server and play with it, all you need is to change the IP to the address where the server is hosted on. The server accepts input data in JSON format as what's written after  **-d**. You need to sepcify the "data-id", "move-in yy, mm, dd" and also the duration of the stay.

Here's a sample json out generated from the query command above:

```
{"photo": "https://a2.muscache.com/ic/pictures/79522229/7d8647fc_original.jpg?interpolation=lanczos-none&size=x_large&output-format=progressive-jpeg&output-quality=70", "desc": "Apartment in New York, United States. The Space I&#x27;m renting 2 rooms in a 3 bedrooms apartment.  The price you see is the price for 1 room (2 ppl) If you want to book both rooms (capacity 4ppl total) you would need to go on both listings below:  https://www.airbnb.com/rooms/244547  htt...", "neighborhood": "UpperEastSide", "price": "$89", "rating": "4.5"}
```

It currently crawls the photo link, description, price, rating and the neighborhood of a specific listing!

The app is now deployed on Heroku. 

```
https://blooming-dawn-3299.herokuapp.com/messages
```


### App Server for answering GET request to the best 50 calculated housing units
Deployed on Heroku. 

```
https://obscure-inlet-8237.herokuapp.com/?food=10&quality=10
```

Returns: 

```
{
  "housing": [
    {
      "data-id": "6363035",
      "latitude": 40.75644645028808,
      "longitude": -73.97718792130098,
      "score": -2380079.2724609375
    },
    {
      "data-id": "1189772",
      "latitude": 40.709574939580364,
      "longitude": -74.00985010287086,
      "score": -1841635.974325214
    },
    {
      "data-id": "6434179",
      "latitude": 40.75788116480949,
      "longitude": -73.97563301520483,
      "score": -1837242.5919049382
    },
    {
      "data-id": "3703146",
      "latitude": 40.708167654234714,
      "longitude": -74.00698532428281,
      "score": -1829162.8472024994
    },
    {
      "data-id": "5941628",
      "latitude": 40.711103002352644,
      "longitude": -74.00872986040642,
      "score": -1802510.9220441156
    },
    {
      "data-id": "6210393",
      "latitude": 40.71009553877744,
      "longitude": -74.00963348887636,
      "score": -1793664.6915218257
    },
    {
      "data-id": "3003664",
      "latitude": 40.710857368832116,
      "longitude": -74.00815042174034,
      "score": -1770013.6761457757
    },
    {
      "data-id": "6311123",
      "latitude": 40.705008005415934,
      "longitude": -74.01005478568406,
      "score": -1741005.5309057524
    },
    {
      "data-id": "2265819",
      "latitude": 40.70637326090316,
      "longitude": -74.00667042253328,
      "score": -1739296.4076178777
    },
    {
      "data-id": "3655783",
      "latitude": 40.713517684928085,
      "longitude": -74.0089329882059,
      "score": -1734119.961413798
    },
    {
      "data-id": "1288089",
      "latitude": 40.71243367061787,
      "longitude": -74.00714631008867,
      "score": -1728107.2104332452
    },
    ......
    ......
    ......
    {
      "data-id": "3561338",
      "latitude": 40.75528253018429,
      "longitude": -73.97434191401072,
      "score": -1722076.831548375
    },
    {
      "data-id": "3349376",
      "latitude": 40.70634999091482,
      "longitude": -74.01256727924556,
      "score": -1717908.9860997545
    },
    {
      "data-id": "6453428",
      "latitude": 40.705141962195974,
      "longitude": -74.00767868993651,
      "score": -1714320.8012301712
    },
    {
      "data-id": "3469213",
      "latitude": 40.707030230505175,
      "longitude": -74.00651982214264,
      "score": -1713282.1724242885
    },

    {
      "data-id": "6391204",
      "latitude": 40.706357422045606,
      "longitude": -74.00599517026578,
      "score": -1641365.1759601478
    }
  ]
}
```

This is for use of page 2 of the Android application. Activity on Page 2 makes a GET request to the heroku server and render the page. 

