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

    def pre-processing(self):
        pass

if __name__ == '__main__':
    main()