from app import app
from flask import render_template
import datetime


NOW = datetime.datetime.now()
CRAWLDATE = datetime.date(2019,2,12)

@app.route('/')
@app.route('/index')
def index():
    lastCrawl = {'CrawlTime':CRAWLDATE}
    data = [
    {       

            'mountain':'keystone',
            'day' : NOW.strftime('%Y/%m/%d'),
            'snow': {'day':'3-4'},
            'temp': {'day':'20 deg C'}
    },
    {
             
            'mountain':'ArapahoeBasin',
            'day' : 'fake date',
            'snow': {'day':'3-4'},
            'temp': {'day':'5'}
    }
    ]

    return  render_template('index.html', title = 'Arctic Spider', \
                 lastCrawl = lastCrawl, data=data)
