#! /usr/bin/env python3

import pickle
import sys

def dePickle():
    pickle_in = open('./vault/data.pickle','rb')
    pickledFile = pickle.load(pickle_in)
    #pickle_in.close()
    return pickledFile

def clean():
    data = dePickle()
    error = data.pop('error',None)
    print(error)
    _resort = []
    _date = []
    _snow = []
    _temp = []
    
    # get the list of resorts
    for field in data:
        print(field)
        print(data[field]['snow']) 

    return


def setConfig():
    CONFIG = []
    with open('./vault/config','r') as d:
        data = d.readlines()
        for line in data:
            line.strip()
            CONFIG.append(line.strip().split())
    print(CONFIG[0][1])
    return

def main():
    return setConfig()

if __name__ == '__main__':
    main()
