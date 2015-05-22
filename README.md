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
**curl -H Content-type: application/json -X POST http://127.0.0.1:5000/messages -d '{"id":"246030", "yr":"2015", "month":"05", "day":"16", "duration":"1"}'**
```

The above command can tell the server to crawl the page that contains detail data of a listing.

If you want to try to launch the server and play with it, all you need is to change the IP to the address where the server is hosted on. The server accepts input data in JSON format as what's written after  **-d**. You need to sepcify the "data-id", "move-in yy, mm, dd" and also the duration of the stay.

Here's a sample json out generated from the query command above:

```
{"photo": "https://a2.muscache.com/ic/pictures/79522229/7d8647fc_original.jpg?interpolation=lanczos-none&size=x_large&output-format=progressive-jpeg&output-quality=70", "desc": "Apartment in New York, United States. The Space I&#x27;m renting 2 rooms in a 3 bedrooms apartment.  The price you see is the price for 1 room (2 ppl) If you want to book both rooms (capacity 4ppl total) you would need to go on both listings below:  https://www.airbnb.com/rooms/244547  htt...", "neighborhood": "UpperEastSide", "price": "$89", "rating": "4.5"}
```


It currently crawls the photo link, description, price, rating and the neighborhood of a specific listing!


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
      "data-id": "5837754",
      "latitude": 40.756250162839905,
      "longitude": -73.97782329029064,
      "score": -2340491.6937945066
    },
    {
      "data-id": "6120311",
      "latitude": 40.70717021720173,
      "longitude": -74.00939477976024,
      "score": -2120260.8281972264
    },
    {
      "data-id": "4531110",
      "latitude": 40.707116487426134,
      "longitude": -74.01016495597399,
      "score": -2113264.230474732
    },
    {
      "data-id": "5387111",
      "latitude": 40.70649136092825,
      "longitude": -74.00913036933872,
      "score": -2112130.366396231
    },
    {
      "data-id": "6141815",
      "latitude": 40.707128175714566,
      "longitude": -74.01169364890458,
      "score": -2060309.9730276465
    },
    {
      "data-id": "1171259",
      "latitude": 40.70730665230217,
      "longitude": -74.0083092770456,
      "score": -2044419.9136097822
    },
    {
      "data-id": "4435633",
      "latitude": 40.7062883698545,
      "longitude": -74.00873769622353,
      "score": -2043262.21442074
    },
    {
      "data-id": "2107952",
      "latitude": 40.705967026595886,
      "longitude": -74.01084840372751,
      "score": -2024964.049897471
    },
    {
      "data-id": "6456848",
      "latitude": 40.70630782656295,
      "longitude": -74.00797991978152,
      "score": -2001124.9496995946
    },
    {
      "data-id": "818252",
      "latitude": 40.70619656199712,
      "longitude": -74.00799078594419,
      "score": -2000814.154988789
    },
    {
      "data-id": "5579886",
      "latitude": 40.70576131040194,
      "longitude": -74.0107407696141,
      "score": -1997670.2292940523
    },
    {
      "data-id": "3541464",
      "latitude": 40.70555525767237,
      "longitude": -74.00989893056217,
      "score": -1996857.9050736497
    },
    {
      "data-id": "4909223",
      "latitude": 40.70830801372377,
      "longitude": -74.00779985841642,
      "score": -1986826.7582861762
    },
    {
      "data-id": "5810313",
      "latitude": 40.70540273994572,
      "longitude": -74.00929772084676,
      "score": -1984146.0522608822
    },
    {
      "data-id": "5796537",
      "latitude": 40.70662773485382,
      "longitude": -74.00803931653336,
      "score": -1975476.8736172565
    },
    {
      "data-id": "5810269",
      "latitude": 40.70674512012721,
      "longitude": -74.00782082614991,
      "score": -1973022.0543175489
    },
    {
      "data-id": "56189",
      "latitude": 40.707263986477706,
      "longitude": -74.0075528281792,
      "score": -1970927.5440788558
    },
    {
      "data-id": "3800051",
      "latitude": 40.71058347509196,
      "longitude": -74.01028059638412,
      "score": -1956698.22997416
    },
    {
      "data-id": "3402474",
      "latitude": 40.70764857192294,
      "longitude": -74.00760954720711,
      "score": -1946434.1782343145
    },
    {
      "data-id": "6074676",
      "latitude": 40.70532776006912,
      "longitude": -74.0095787675258,
      "score": -1920006.089643415
    },
    {
      "data-id": "6421158",
      "latitude": 40.70618619662481,
      "longitude": -74.00729559645967,
      "score": -1907607.9112081514
    },
    {
      "data-id": "5758072",
      "latitude": 40.7108297552044,
      "longitude": -74.00964207316001,
      "score": -1907141.2573481388
    },
    {
      "data-id": "6092991",
      "latitude": 40.70551887498018,
      "longitude": -74.00786461043951,
      "score": -1906106.5334613677
    },
    {
      "data-id": "4889629",
      "latitude": 40.70576489769266,
      "longitude": -74.00762383496061,
      "score": -1882247.343518244
    },
    {
      "data-id": "505915",
      "latitude": 40.705357697812886,
      "longitude": -74.00864224749407,
      "score": -1869801.063015312
    },
    {
      "data-id": "2230982",
      "latitude": 40.70511049411266,
      "longitude": -74.00942583381034,
      "score": -1860478.5520094563
    },
    {
      "data-id": "4639847",
      "latitude": 40.70938158936421,
      "longitude": -74.01107486005235,
      "score": -1855602.9622132257
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
      "data-id": "6257250",
      "latitude": 40.70790738839034,
      "longitude": -74.00620261549318,
      "score": -1704698.3258054801
    },
    {
      "data-id": "6290837",
      "latitude": 40.70764011771559,
      "longitude": -74.00662660762003,
      "score": -1703081.0316389264
    },
    {
      "data-id": "2621191",
      "latitude": 40.75670420566063,
      "longitude": -73.97330169736273,
      "score": -1695565.1801801804
    },
    {
      "data-id": "4121173",
      "latitude": 40.70499181489662,
      "longitude": -74.00818582250794,
      "score": -1666503.6052588602
    },
    {
      "data-id": "1917923",
      "latitude": 40.755734727425285,
      "longitude": -73.97372893710147,
      "score": -1663587.5674188226
    },
    {
      "data-id": "5338034",
      "latitude": 40.71193692685747,
      "longitude": -74.00700026375918,
      "score": -1661512.8546332894
    },
    {
      "data-id": "3695178",
      "latitude": 40.75496372299712,
      "longitude": -73.97405951456342,
      "score": -1651425.3301276122
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

