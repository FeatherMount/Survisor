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
    { "_id" : ObjectId("55469ad5300446310dd2c3c3"), "name" : "Cookshop", "rating" : 4, "latitude" : 40.7454262, "longitude" : -74.0056076, "zip" : 10001 }
```


NOTES:
Required lib to run the program:
    json_simple-1.1.jar
    scribe-1.3.5.jar
    mongo-java-driver-2.11.3.jar

### NYC311