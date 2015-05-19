import numpy as np
import pymongo
import matplotlib.pyplot as plt
from matplotlib.pyplot import show

# CONST_PATCH_SIZE is an important parameter can can determine the 
# data pre-processing efficiency
CONST_PATCH_SIZE = 0.005 
CONST_EAST_BOUND = 41.2903
CONST_WEST_BOUND = 40.4677
CONST_NORTH_BOUND = -74.4375
CONST_SOUTH_BOUND = -73.3281

def main():
    # first thing needs to be done is to find a suitable granularity
    # scatter plot all latitude and longitude
    cleaner = DataCleaner()
    # use the following three function calls to check the density of the data
    #cleaner.plot311()
    #cleaner.plotAb()
    #cleaner.plotYelp()
    cleaner.pre_process()


class DataCleaner(object):
    """
    This class is a utility class to clea up data, extract features from MongoDB
    """
    def __init__(self):
        mongoUri = 'mongodb://zhou:cu6998@ds061711.mongolab.com:61711/survisor'
        self.client = pymongo.MongoClient(mongoUri)
        self.db = self.client.get_default_database()
        self.ablists = self.db['ablists']
        self.yelp = self.db['yelpDB']
        self.complaint = self.db['db311']

    def plot311(self):
        lat = np.array([])
        lng = np.array([])
        i = 0
        for complaint in self.complaint.find():
            i = i + 1
            # un-geotagged record
            if not(complaint['lat'] and complaint['long']):
                continue
            temp_lat = float(complaint['lat'])
            temp_lng = float(complaint['long'])
            # out of New York or mislabled junk data
            if temp_lat > CONST_EAST_BOUND or temp_lat < CONST_WEST_BOUND:
                continue
            if temp_lng > CONST_SOUTH_BOUND or temp_lng < CONST_NORTH_BOUND:
                continue
            lat = np.append(lat, temp_lat)
            lng = np.append(lng, temp_lng)
            if (i > 5000):
                break
        plt.scatter(lat, lng, s = 2)
        show()

    def plotAb(self):
        lat = np.array([])
        lng = np.array([])
        i = 0
        for bnb in self.ablists.find():
            i = i + 1
            # un-geotagged record
            if not(bnb['data-lat'] and bnb['data-lng']):
                continue
            temp_lat = float(bnb['data-lat'])
            temp_lng = float(bnb['data-lng'])
            # out of New York or mislabled junk data
            if temp_lat > CONST_EAST_BOUND or temp_lat < CONST_WEST_BOUND:
                continue
            if temp_lng > CONST_SOUTH_BOUND or temp_lng < CONST_NORTH_BOUND:
                continue
            lat = np.append(lat, temp_lat)
            lng = np.append(lng, temp_lng)
            if (i > 5000):
                break
        plt.scatter(lat, lng, s = 2)
        show()

    def plotYelp(self):
        lat = np.array([])
        lng = np.array([])
        i = 0
        for restaurant in self.yelp.find():
            i = i + 1
            # un-geotagged record
            if not(restaurant['latitude'] and restaurant['longitude']):
                continue
            temp_lat = float(restaurant['latitude'])
            temp_lng = float(restaurant['longitude'])
            # out of New York or mislabled junk data
            if temp_lat > CONST_EAST_BOUND or temp_lat < CONST_WEST_BOUND:
                continue
            if temp_lng > CONST_SOUTH_BOUND or temp_lng < CONST_NORTH_BOUND:
                continue
            lat = np.append(lat, temp_lat)
            lng = np.append(lng, temp_lng)

            if (i > 5000):
                break
        plt.scatter(lat, lng, s = 2)
        show()

    def pre_process(self):
        # obtain all the data-id first
        i= 0
        for data_id in self.ablists.distinct("data-id"):
            if (i == 2):
                break
            list_item = self.ablists.find_one({"data-id":data_id})
            latitude = float(list_item["data-lat"])
            longitude = float(list_item["data-lng"])
            temp = {}
            temp["data-id"] = data_id
            temp["latitude"] = latitude
            temp["longitude"] = longitude

            #air quality (na)
            #building (nb)
            #electrical (ne)
            #noise (nn)
            #rodent (nrdnt)
            #sewer (ns)
            #sanitaion (nsttn)
            #street (nstrt)
            #water (nw)

            #number of restaurants (nrst)
            #average rating (ar)

            na = 0
            nb = 0
            ne = 0
            nn = 0
            nrdnt = 0
            ns = 0
            nsttn = 0
            nstrt = 0
            nw = 0
            nrst = 0
            ar = 0

            for entry in self.complaint.find():
                if entry["lat"] is None or entry["lat"] == "":
                    continue
                if ((float(entry["lat"])-latitude)*(float(entry["lat"])-latitude) + 
                    (float(entry["long"])-longitude)*(float(entry["long"])-longitude) < CONST_PATCH_SIZE * CONST_PATCH_SIZE):
                    if "Noise" in entry["type"]:
                        nn = nn + 1
                    if entry["type"] == "Air Quality":
                        na = na + 1
                    if entry["type"] == "Building/Use":
                        nb = nb + 1
                    if entry["type"] == "Electrical":
                        ne = ne + 1
                    if entry["type"] == "Rodent":
                        nrdnt = nrdnt + 1
                    if entry["type"] == "Sewer":
                        ns = ns + 1
                    if entry["type"] == "Sanitaion Condition":
                        nsttn = nsttn + 1
                    if entry["type"] == "Street Condition":
                        nstrt = nstrt + 1
                    if entry["type"] == "Water System":
                        nw = nw + 1
            temp["na"] = na
            temp["nn"] = nn
            temp["nb"] = nb
            temp["ne"] = ne
            temp["nrdnt"] = nrdnt
            temp["ns"] = ns
            temp["nsttn"] = nsttn
            temp["nstrt"] = nstrt
            temp["nw"] = nw
            for entry in self.yelp.find():
                if (entry["latitude"]) is None or entry["latitude"] == "":
                    continue
                if ((float(entry["latitude"])-latitude)*(float(entry["latitude"])-latitude) + 
                    (float(entry["longitude"])-longitude)*(float(entry["longitude"])-longitude) < CONST_PATCH_SIZE * CONST_PATCH_SIZE):
                    nrst = nrst + 1
                    ar = ar + entry["rating"]

            ar = ar / nrst
            temp["nrst"] = nrst
            temp["ar"] = ar

            print(temp)
            i = i + 1
    #    # db.ablists.distinct("data-lng",{"data-lng":{$lt: "-73.95", $gt: "-73.92"}, "data-lat":{$lt : "40.82", $gt: "40.81"}})

if __name__ == '__main__':
    main()
