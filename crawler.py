#! /usr/bin/env python3
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from random import shuffle
import random
import pickle
import sys
import time

######################## Crawler Settings ########################


def setConfig():
    '''
    Desc     : Pulls crawler settings from the .config file located
                in the ./vault directory

    Required : ./vault/.config
    
    Format   : 'foo: bar' where foo is the description and 
               bar is the value
    
    Output   : list of lines from file
    
    '''

    CONFIGS = []
    
    with open('./vault/.config','r') as f:
        data = f.readlines()
        for line in data:
            CONFIGS.append(line.strip().split())

    return CONFIGS

UA = UserAgent() # generate a random user agent
URL = setConfig()[0][1] # first line second element


######################## Crawler Settings ########################


def crawl():

    # grab the list of resorts
    pickle_in = open('./vault/resortList.pickle', 'rb')
    pickledFile = pickle.load(pickle_in)
    
    # remove white space to facilitate the search
    resortList = []
    data = {}
    errorlog=[]

    for resorts in pickledFile:
        resortList.append(''.join(resorts))
    shuffle(resortList)

    for resort in resortList:
        try:
            print('crawling on {} \n'.format(resort))

            req = Request(URL + resort) 
            req.add_header('User-Agent', UA.random)    

            req_doc = urlopen(req).read().decode('utf8')
            soup = BeautifulSoup(req_doc,'html.parser')
            
            data_tbl = soup.select('.dnum')
            snow_tbl = soup.select('.us')
            high_tbl = soup.select('.high') 
            low_tbl = soup.select('.low')
            
            #for i in data_tbl:
            #    print(i.getText().split())

            date_tbl = turnToList(data_tbl)[:5]
            snow_tbl = turnToList(snow_tbl)
            high_tbl  = turnToList(high_tbl)
            low_tbl = turnToList(low_tbl)

            # store into dictionary
            data[resort] = {'date':date_tbl,'snow':snow_tbl,'h_temp':high_tbl,'l_temp':low_tbl}

            print(data[resort])
                 
            print('completed crawling on {}...\n'.format(resort))
        except:
            print('error retrieving data for {}\n'.format(resort))
            errorlog.append(resort)
            pass

        time.sleep(30)

    data['error'] = errorlog
    #offload data into a pickle
    pickle_out = open('../vault/data.pickle','wb')
    pickle.dump(data,pickle_out)
    pickle_out.close()
    print('crawler completed!')
    
    return

def turnToList(soup):
    table = []
    for i in soup:
        table.append(i.getText().split())
    return table
    

def main():
    crawl()

if __name__=='__main__':
      main()
