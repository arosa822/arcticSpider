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
        
        date = data[field]['date']
        snow = data[field]['snow']
        lTemp = data[field]['l_temp']

        hTemp = data[field]['h_temp']
        
        
        # first element is night for the current day

        snowDay = snow[1::2]
        snowNight = snow[0::2]
        
        print('-------------------------------------')
        print(field)
        
        print(date)
        print('Low Temp:\n{}'.format(lTemp))
        print('High Temp:\n{}'.format(hTemp))

        print('Day-snow:\n{}'.format(snowDay))
        
        print('Night-snow:\n{}'.format(snowNight))
        
        
        #print(snowDay)
        
    
#        snowDay = snow[6:]

    return

def main():
    return clean()

if __name__ == '__main__':
    main()
