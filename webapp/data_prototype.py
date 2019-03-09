from app import db
from app.models import User,Resort,Conditions
import os
import re

DIR = '../vault'

def addUser(name,email):
    u = User(username= name,email = email)
    print(User)
    print(u)
    return

def addResort(location):
    r = Resort(location = location)
    print(Resort)
    print(r)

def searchDir(directory):
    '''This fuction performs a search on files 
    in the vault, filters the resulting list
    to contain only those which have been assigned 
    a number, then selects the most recent addition
    
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
    return results[0]

def main():
    addUser('alex','alex.com')
    addResort('keystone')
    print(searchDir(DIR))

    return

if __name__=='__main__':
    main()
