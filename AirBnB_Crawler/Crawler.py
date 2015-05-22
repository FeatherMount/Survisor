import urllib.request
from bs4 import BeautifulSoup as bs
import datetime
from datetime import timedelta
import pymongo
import time

CONST_DATE_WINDOW = 30
CONST_DURATION_WINDOW = 1

class Crawler(object):
    """
    Crawler crawls for all the NYC AirBnB price listings
    From the current date on for a month
    """
    def __init__(self):
        mongoUri = 'mongodb://zhou:cu6998@ds061711.mongolab.com:61711/survisor'
        self.client = pymongo.MongoClient(mongoUri)
        self.db = self.client.get_default_database()
        self.ablists = self.db['ablists']
        
    def crawlBatch(self):
        currDate = datetime.date.today()
        baseDate =  currDate
        increment = timedelta(days=1)
        for i in range(CONST_DATE_WINDOW):
            duration = timedelta(days=1)
            for j in range(CONST_DURATION_WINDOW):
                self.crawl(baseDate, duration)
                duration = duration + increment
            baseDate = baseDate + increment
        self.client.close()

    def crawl_one(self, _id, checkinDate, duration):
        baseUrl = "https://www.airbnb.com/rooms/{}?checkin={}%2F{}%2F{}&checkout={}%2F{}%2F{}"
        #url = "https://www.airbnb.com/rooms/246030?checkin=05%2F15%2F2015&checkout=05%2F16%2F2015&s=cbcd"
        checkoutDate = checkinDate + duration
        url = baseUrl.format(_id, checkinDate.month, checkinDate.day, checkinDate.year,
                        checkoutDate.month, checkoutDate.day, checkoutDate.year)

        try:
            request = urllib.request.Request(url, headers={'User-Agent' : "Magic Browser"})
            response = urllib.request.urlopen(request)
            soup = bs(response.read())
            price = soup.find('div', {'class':'subnav-container'}).find('span', {'class' : 'price-amount h3'})
            for p in price:
                price = p.replace("\n", "").replace(" ", "")
            neighborhood = soup.find('h3', {'class':'seo-text'})
            for nb in neighborhood:
                neighborhood = nb.replace("\n", "").replace(" ", "")
            rating = "n/a"
            metas = soup.findAll('meta')
            for meta in metas:
                if not meta.get('property'):
                    continue
                elif meta['property'] == "airbedandbreakfast:rating":
                    rating = meta['content']
                elif meta['property'] == "og:image":
                    photo = meta['content']
                elif meta['property'] == "og:description":
                    desc = meta['content']
            output = {}
            output['price'] = price
            output['neighborhood'] = neighborhood
            output['rating'] = rating
            output['photo'] = photo
            output['desc'] = desc
            output['url'] = url
            #print(output)
            return output
        except:
            print("processing one URL error: {}".format(url))

    def crawl(self, currDate, duration):
        checkinDate = currDate;
        checkoutDate = checkinDate + duration
        #baseUrl = ("https://www.airbnb.com/s/New-York--NY--United-States?"
        baseUrl = ("https://www.airbnb.com/s/Manhattan--New-York--NY--United-States?"
                "checkin={}%2F{}%2F{}&checkout={}%2F{}%2F{}"
                "&source=bb&ss_id=troj9a2t&page={}")
        url = baseUrl.format(checkinDate.month, checkinDate.day, checkinDate.year, 
                        checkoutDate.month, checkoutDate.day, checkoutDate.year, 1)
        # obtain totalPage here
        request = urllib.request.Request(url, headers={'User-Agent' : "Magic Browser"})
        response = urllib.request.urlopen(request)
        soup = bs(response.read())
        pagingInfo = soup.find('div', {'class':"pagination"})
        allLists = pagingInfo.findAll('li') # confusing name here: list refers to <li>
        totalPage = int(allLists[len(allLists) - 2].a.string)
        
        print('there are totally {} pages for {} and {}'.format(totalPage, checkinDate, duration))        
        # execute the crawler
        for i in range(totalPage):
            page = i + 1
            url = baseUrl.format(checkinDate.month, checkinDate.day, checkinDate.year, 
                        checkoutDate.month, checkoutDate.day, checkoutDate.year, 
                        page)            
            request = urllib.request.Request(url, headers={'User-Agent' : "Magic Browser"})
            # in order not to be banned sleep for a second here
            time.sleep(1);
            try:
                response = urllib.request.urlopen(request, timeout = 5)
                soup = bs(response.read())
                listings = soup.findAll('div', {'class':"listing"})
                print ('page {}: processing {} items'.format(page, len(listings)))
                for listing in listings:
                    # print(listing.attrs)
                    # push listing.attrs to MongoDB
                    self.ablists.insert(listing.attrs)
            except:
                print("processing error: {}".format(url))

if __name__ == '__main__':
    crawler = Crawler()
    crawler.crawlBatch()
    #currDate = datetime.date.today()
    #duration = timedelta(days=1)
    #crawler.crawl_one("246030", currDate, duration)
