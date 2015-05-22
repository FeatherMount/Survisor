import os
import flask
from flask import Flask
from flask import request
import WeightedSorter as ws

app = Flask(__name__)

@app.route('/', methods = ['GET',])
def AppServerRank():
    try:
        assert request.path == '/'
        assert request.method == 'GET'
    except:
        return 'Invalid request'
    try:
        mega_food = request.args.get('food','')
        mega_quality = request.args.get('quality','')
        sorter = ws.WeightedSorter()
        response = sorter.getRanked(int(mega_food), int(mega_quality))
    except:
        return 'Server down!'
    else:
        dicts = []
        for tup in response:
            item = {'score':tup[0], 'data-id':tup[1], 'latitude':tup[2], 'longitude':tup[3]}
            dicts.append(item)
        return flask.jsonify(housing=dicts)

if __name__=='__main__':
    app.run()