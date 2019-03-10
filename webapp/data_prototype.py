from app import db
from app.models import User,Resort,Conditions
import os
import re
import pickle

DIR = '../vault'
RESORTLIST = DIR + '/' + 'resortList.pickle'
RESORT_LIST = '../vault/resortList.pickle'


def addResort(location):
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


def main():
    return

if __name__=='__main__':
    main()
