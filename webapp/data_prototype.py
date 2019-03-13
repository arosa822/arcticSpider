#! /usr/bin/env python3
'''
Description of methods here:
    * process for adding resort list (import from interpreter) 
        - only needs to be done once, this will link to resort data obtained

Todo:
    add logs for collecting errors. sertain resorts in the list do 
    not match 'resort name' of data obtained.  

    - generate process for appending resort table with data obtained ('key'
      values?? 

'''
from app import db
from app.models import User,Resort,Conditions
import os
import re
import pickle
from datetime import datetime, date
import sys

#folder/file locations
DIR = '../vault'
RESORT_LIST = '../vault/resortList.pickle'

# extract the data from vault location
def dePickle(fileLocation):
    pickle_in = open(fileLocation,'rb')
    pickledFile = pickle.load(pickle_in)
    return pickledFile

# helper method to concatenate scraper results
def combine(field):
    combinedList = []
    for item in field:
            for element in item:
                combinedList.append(element)
    return combinedList

def processData(fileLocation):
    print('processing data for {}'.format(fileLocation))
    data = dePickle(fileLocation)
    error = data.pop('error',None)
    # get the current year to append to datetime objects
    year = date.today().strftime('%Y')
    # initialize dictionary to hold all the data
    # need to create seperate dictionary items for each 
    # location as the program iterates over each location
    processed = {}

    for key in data:
        # initialize dictionaries for each location
        processed[key]={}
        # organize the data into seperate fields
        Date = combine(data[key]['date'])
        snowDay = combine(data[key]['snow'][0::2])
        snowNight = combine(data[key]['snow'][1::2])
        lTemp = combine(data[key]['l_temp'])
        hTemp = combine(data[key]['h_temp'])
        info = combine(data[key]['past24'])
        
        # process datetimes
        Date = [i + '/' + year for i in Date]        
        # convert string dates to datetime objects
        n = 0
        for i in Date:
            Date[n] = datetime.strptime(i,'%m/%d/%Y')
            n+=1
        # stash the datetime objects in dictionary
        processed[key]['date']=Date

        # process strings and remove unwanded characters for snow Data
        snowDay = list(map(lambda x:x.strip('\"').split('-'), snowDay))
        snowNight = list(map(lambda x:x.strip('\"').split('-'),snowNight))
        # remove '-' character, keep grouping and convert to int
        snowDay = list(map(lambda x: [int(i) for i in x], snowDay))
        snowNight = list(map(lambda x: [int(i) for i in x], snowNight))
        # stash the processed data in dictionary
        processed[key]['snowDay']=snowDay
        processed[key]['snowNight']=snowNight

        # replace degree F swymbol from temps using list comprehension
        lTemp = [s.replace(u'\N{DEGREE SIGN}F', '') for s in lTemp]
        hTemp = [s.replace(u'\N{DEGREE SIGN}F', '') for s in hTemp]
        # convert strings to int
        lTemp = list(map(lambda x:int(x),lTemp))
        hTemp = list(map(lambda x: int(x),hTemp))
        # stash the processed data in the dictionary
        processed[key]['lTemp']=lTemp
        processed[key]['hTemp']=hTemp

    return processed

#helper function 
def getResortList():
    # open the pickled file
    pickle_in = open(RESORT_LIST, 'rb')
    pickledFile = pickle.load(pickle_in)

    resortList = []
    
    # process the data
    for resorts in pickledFile:
        resortList.append(''.join(resorts))

    return resortList


def addResort(location):
    '''Helper function - execute
    externally, only do this once if initiating database
    we only need to update the Resort table once. 
    :param str location: relative loaction to list of resorts
    '''
    r = Resort(location = location)
    db.session.add(r)
    return

def searchDir(directory):
    '''This fuction performs a search on files 
    in the vault and returns the most recently 
    scraped data pickle file.
    :param str directory: relative directory to search
    :return str results[0]: most recent crawl result
    '''
    results = []
    for root, dirs, files in os.walk(directory):
        for filename in files:
            if filename.endswith('.pickle'):
                results.append(filename)

    #only return files with a number associated
    results = list(filter(lambda x: bool(re.search(r'\d',x)),results))
    results.sort(reverse=True)
    result = DIR + '/' + results[0] 
    return result

def dbResortList():
    d = {}
    resortdb = Resort.query.all()
    print('resort index:')
    for r in resortdb:
        print(r.id,r.location)
        d[r.location]=r.id
    return d        

def iterateData(dic,key):
    '''iterates through one of the dictionary elements given
    a specific key
    :param:
    '''
    
    
    return 
def main():
    # searh for latest data scrape
    latestData = searchDir(DIR)
    # process the raw data
    processed =  processData(latestData)
    # create an index for pushing processed data
    index = dbResortList()
    
    # stash the data in the db
    resortdb  = Resort.query.all()
    # key error list containter 
    err = []
    for r in resortdb:
       
        '''insert explanation here '''
        try:

            print('query: {}'.format(r.location))
            print(r)
            #print(processed[r.location])
            print('\n')
            
            #iterate over the days
            days = processed[r.location]['date']
            snowDay = processed[r.location]['snowDay']
            snowNight = processed[r.location]['snowNight']
            lTemp = processed[r.location]['lTemp']
            hTemp = processed[r.location]['hTemp']
            

            for d in range(0,len(days)):
                #print(snowDay[d][-1])
                #print(snowNight[d][-1])
                #print(lTemp[d])
                #print(hTemp[d])
                #print(days[d])
                data  = Conditions(snowDay = snowDay[d][-1],
                                snowNight = snowNight[d][-1],
                                ltemp = lTemp[d],
                                htemp = lTemp[d],
                                timestamp = days[d],
                                loc = r)
                db.session.add(data)

            
                #print("success")
        except KeyError:
            'query by name in list, some names do not exist in database'
            print('\n   key error...\n')
            #err.append(r.location)
            pass
        except:
            print('some other error occured')
    
    #print('errors encountered:\n {}\n'.format(err)) 
    #print('query index:\n{}'.format(index))
    

    conditions = Conditions.query.all()
    for c in conditions:
        print(c.loc.location,c.timestamp,c.snowDay,c.snowNight)
    
    u = input("commit data to database? (y/n) \n")
    if u == 'y':
        print('commiting data to database...\n')
        db.session.commit()
    else:
        pass
    return 

if __name__=='__main__':
    sys.exit(main())
