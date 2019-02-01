import flask 
from flask import request,jsonify

app = flask.Flask(__name__)
app.config["DEBUG"] = True

forcasts = [
        {'id': 0, 'resort': 'keystone','day': 'friday','snow':'5-10'}, 
        {'id': 1, 'resort': 'keystone','day': 'friday','snow':'5-10'}
]
        
@app.route('/', methods = ['GET'])
def home():
    return "<h1> ArcticSpider results </h1> <p> This site is a prototype API for obtaining results from the arcticSpider web crawler </p>"


@app.route('/api/v1/resources/forcasts/all', methods=['GET'])
def api_all():
    return jsonify(forcasts)


@app.route('/api/v1/resources/forcasts' , methods =['GET'])
def api_id():
    # check if an ID was provided as part of the URL
    # if ID is provided, assign it to a variable.
    # if no ID is provided, display an error in the browser
    if 'id' in request.args:
        id = int(request.args['id'])
    else: 
        return '<h1> Error:</h1> <p>No id field provided. Please specify an ID</p>'

    # create an empty list for our results

    results = []

    # loop through the data and match results that fit the requested ID

    for forcast in forcasts:
        if forcast['id'] == id:
            results.append(forcast)

    # use the jsonify function from Flask to convert our list of
    # python dictionaries to the JSON format
    # example : 127.0.0.1:5000/api/v1/resources/forcasts?id=0
    return jsonify(results)
app.run()

