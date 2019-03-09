from app import db
from app.models import User,Resort,Conditions
import os

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
    results = []
    for root, dirs, files in os.walk(directory):
        for filename in files:
            if filename.endswith('.pickle'):
                print(filename)
                results.append(filename)

    return results

def main():
    addUser('alex','alex.com')
    addResort('keystone')
    print(searchDir(DIR))

    return

if __name__=='__main__':
    main()
