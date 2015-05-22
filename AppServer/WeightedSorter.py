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
CONST_TOP = 50


class WeightedSorter(object):
    """
    This class is to sort in response to the HTTP request from the android device
    score = mega_food * (50 * nrst + 50 * ar) - (
    0.5 * mega_quality * 20 * na + 5 * nb + 10 * ne + mega_quality * 20 * nn + mega_quality * 30 * nrdnt + 
    50 * ns + 25 * nsttn + mega_quality * 5 * nstrt + 15 * nw)

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

    """
    def __init__(self):
        mongoUri = 'mongodb://zhou:cu6998@ds061711.mongolab.com:61711/survisor'
        client = pymongo.MongoClient(mongoUri)
        db = client.get_default_database()
        features = db['features']
        self.cached = []
        for item in features.find():
            self.cached.append(item)

    def getRanked(self, mega_food, mega_quality):
        score = []
        for item in self.cached:
            temp = mega_food * (item["nrst"] * 50 + item["ar"] * 50)
            temp -= (0.5 * mega_quality * 20 * item["na"] + 5 * item["nb"] + 10 * item["ne"] + 
                mega_quality * 20 * item["nn"] + mega_quality * 30 * item["nrdnt"] + 
                50 * item["ns"] + 25 * item["nsttn"] + mega_quality * 5 * item["nstrt"] + 15 * item["nw"])
            # note that the sign of temp is reversed to simplify sorting
            score.append((-temp, item["data-id"], item["latitude"], item["longitude"]))
        score = (sorted(score))[0:CONST_TOP]
        return score

def main():
    ws = WeightedSorter()
    print(ws.getRanked(0, 50))

     

if __name__ == '__main__':
    main()
