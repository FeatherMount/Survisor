from flask import Flask, url_for, request
from Crawler import Crawler
import json
import datetime

app = Flask(__name__)

@app.route('/messages', methods = ['POST', 'GET'])
def crawl_one():
    if request.method == 'GET':
        return "Hello"
    elif request.method == 'POST':
        req = request.get_json()
        crawler = Crawler()
        currDate = datetime.date(int(req['yr']), int(req['month']), int(req['day']))
        duration = datetime.timedelta(days=int(req['duration']))
        l_id = req['id']
        out = crawler.crawl_one(l_id, currDate, duration)
        return json.dumps(out)

if __name__ == '__main__':
    app.debug = True 
    app.run()
