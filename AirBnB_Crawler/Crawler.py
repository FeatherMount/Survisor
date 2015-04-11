import urllib.request
from bs4 import BeautifulSoup as bs
import datetime
from datetime import timedelta

class Crawler(object):
    """
    Crawler crawls for all the NYC AirBnB price listings
    From the current date on for a month
    """
    def __init__(self, arg):
        self.arg = arg
        
    def crawBatch(self):
        currDate = datetime.date.today()
        baseDate =  currDate
        increment = timedelta(days=1)
        for i in range(30):
            duration = timedelta(days=1)
            for j in range(1):
                crawl(baseDate, duration)
                duration = duration + increment
            baseDate = baseDate + increment

    def crawl(self, currDate, duration):
        checkinDate = currDate;
        checkoutDate = checkinDate + duration
        baseUrl = ("https://www.airbnb.com/s/New-York--NY--United-States?"
                "checkin={}%2F{}%2F{}&checkout={}%2F{}%2F{}"
                "&source=bb&ss_id=troj9a2t")
        url = baseUrl.format(checkinDate.month, checkinDate.date, checkinDate.year, 
                        checkoutDate.month, checkoutDate.date, checkoutDate.year)
        request = urllib.request.Request(url, headers={'User-Agent' : "Magic Browser"})
        response = urllib.request.urlopen(request)
        soup = bs(response.read())
        listings = soup.findAll('div', {'class':"listing"})
        print ('processing {} items'.format(len(listings)))
        for listing in listings:
            itemId = listing.attr['data-id']
            userId = listing.attr['data-user']
            price = listing.attr['data-price']
            lng = listing.attr['data-lng']
            lat = listing.attr['data-lat']
            # update to database


if __name__ == '__main__':
    crawl()