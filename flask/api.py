import flask 
from flask import request,jsonify

app = flask.Flask(__name__)
app.config["DEBUG"] = True

forcast = [
        {'id': 0, 'resort': 'keystone','day': 'friday','snow':'5-10'}, 
        {'id': 1, 'resort': 'keystone','day': 'friday','snow':'5-10'}
]
        
@app.route('/', methods = ['GET'])
def home():
    return "<h1> Crawler Resorts </h1> <p> This site is a prototype API for obtaining results from the arcticSpider web crawler </p>"


@app.route('/api/v1/resources/forcasts/all', methods=['GET'])
def api_all():
    return jsonify(forcast)

app.run()

