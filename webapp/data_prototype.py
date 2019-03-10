from app import db
from app.models import User,Resort,Conditions
import os
import re
import pickle
from datetime import datetime, date


#folder/file locations
DIR = '../vault'
RESORT_LIST = '../vault/resortList.pickle'

# extract the data from vault location
def dePickle(location):
    pickle_in = open(location,'rb')
    pickledFile = pickle.load(pickle_in)
    return pickledFile

# helper method to concatenate scraper results
def combine(field):
    combinedList = []
    for item in field:
            for element in item:
                combinedList.append(element)
    return combinedList

def clearn():
    data = dePickle()
    error = data.pop('error',None)

    year = date.today().strftime('%Y')

    for key in data:
        Date = combine(data[key]['date'])
        snowDay = combine(data[key]['snow'][0::2])
        snowNight = combine(data[key]['snow'][1::2])
        lTemp = combine(data[key]['l_temp'])
        hTemp = combine(data[key]'h_temp'])
        info = combine(data[key]['past24'])

        Date = [i + '/' + year for i in Date]
        
        # convert string dates to datetime objects
        n = 0
        for i in Date:
            Date[n] = datetime.strptime(i,'%m/%d/%Y')
            n+=1



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




def main():
    return

if __name__=='__main__':
    main()
