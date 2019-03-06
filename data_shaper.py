#! /usr/bin/env python3

import pickle
import sys
import itertools
        
def dePickle():
    pickle_in = open('./vault/20190226data.pickle','rb')
    pickledFile = pickle.load(pickle_in)
    #pickle_in.close()
    return pickledFile

def combine(field):
    combinedList = []
    for item in field:
        for element in item:
            combinedList.append(element)
    return combinedList


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
        past24 = data[field]['past24']       
        # first element is night for the current day

        snowDay = snow[0::2]
        snowNight = snow[1::2]
        
        # combine all the elements in the list 
        # [[1,2],[3,4]] => [1,2,3,4]
        snowDay = combine(snowDay)
        snowNight = combine(snowNight) 
        date = combine(date)
        lTemp = combine(lTemp)
        hTemp = combine(hTemp)
        
        # process strings and remove unwanded characters
        snowDay = list(map(lambda x:x.strip('\"').split('-'), snowDay))
        snowNight = list(map(lambda x:x.strip('\"').split('-'),snowNight))
       
        # remove '-' character, keep grouping and convert to int
        snowDay = list(map(lambda x: [int(i) for i in x], snowDay))
        snowNight = list(map(lambda x: [int(i) for i in x], snowNight))
        
        
        # replace degree F swymbol from temps using list comprehension
        lTemp = [s.replace(u'\N{DEGREE SIGN}F', '') for s in lTemp]
        hTemp = [s.replace(u'\N{DEGREE SIGN}F', '') for s in hTemp]
        # convert strings to int
        lTemp = list(map(lambda x:int(x),lTemp))
        hTemp = list(map(lambda x: int(x),hTemp))
        
        print('Resort: {}\n'.format(field))

        print('Dates:\n{}'.format(date))

        print('Low Temp:\n{}'.format(lTemp))

        print('High Temp:\n{}'.format(hTemp))


        print('Day:\n{}'.format(snowDay))
        
        print('Night:\n{}'.format(snowNight))
      
        print('data:\n{}'.format(past24))
        print('--------------------------------------------')
    return

def main():
    return clean()

if __name__ == '__main__':
    sys.exit(main())
