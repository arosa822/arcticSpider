from app import app
from flask import render_template
import datetime


now = datetime.datetime.now()


@app.route('/')
@app.route('/index')
def index():
    mountain = {'mountain':'keystone'}
    data = [
    {
            'day' : now.strftime('%Y/%m/%d'),

            'snow': {'day':'3-4'},
            'temp': {'day':'20 deg C'}
    },
    {
            
            'day' : 'fake date',

            'snow': {'day':'3-4'},
            'temp': {'day':'5'}
    }
    ]
    return  render_template('index.html', title = 'Arctic Spider', mountain = mountain, data=data)
