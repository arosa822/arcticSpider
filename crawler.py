#! /usr/bin/env python3
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from random import shuffle, randint
import random
import pickle
import sys
import time
import logging
import datetime


# keep track of time it takes to execute crawl
start_time = time.time()

now = datetime.datetime.now()
######################## Crawler Settings ########################

logging.basicConfig(filename = 'crawler.log',
                    filemode='a',
                    format = '%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',
                    datefmt = '%Y-%m-%d %H:%M:%S', 
                    level = logging.DEBUG)

logging.info('Crawler initialized..')

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
API_KEY = setConfig()[1][1]

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

        logging.info('Crawling on {}'.format(resort))
        
        print('crawling on {}... \n'.format(resort))
               
        payload = {'key': API_KEY, 'url': URL + resort}
        req_doc = requests.get('http://api.scraperapi.com',params = payload)
        logging.info(req_doc.status_code)

        # typical method for requests when not spoofing proxies
        #req = Request(URL + resort) 
        #req.add_header('User-Agent', UA.random)    
        #req_doc = urlopen(req).read().decode('utf8')
           
        if req_doc.status_code != 200:
                    
            print('error retrieving data for {}\n'.format(resort))
            errorlog.append(resort)
            logging.error('failed to retrieve data from {}'.format(resort))
            logging.error('response code: {}'.format(req_doc.status_code))

        else:
                            
            soup = BeautifulSoup(req_doc.text,'html.parser')
            
            data_tbl = soup.select('.dnum')
            snow_tbl = soup.select('.us')
            high_tbl = soup.select('.high') 
            low_tbl = soup.select('.low')
            past24 = soup.select('.data-box')

            date_tbl = turnToList(data_tbl)[:5] # need only the first 5 entries 
            snow_tbl = turnToList(snow_tbl)
            high_tbl  = turnToList(high_tbl)
            low_tbl = turnToList(low_tbl)
            past24_tbl = turnToList(past24)

            # store into dictionary
            data[resort] = {'date':date_tbl,'snow':snow_tbl,'h_temp':high_tbl,'l_temp':low_tbl,'past24':past24_tbl}

            print(data[resort])                 
            print('\ncompleted crawling on {}.\n'.format(resort))

        time.sleep(randint(15,40))
    
    # stash data and errors 
    data['error'] = errorlog
    pickle_out = open('./vault/'+now.strftime('%Y%m%d')+'data.pickle','wb')
    pickle.dump(data,pickle_out)
    pickle_out.close()

    print('crawler completed!')        
    logging.info('Crawl completed') 
    logging.info('Crawler took {}s to complete ------------ '.format( (time.time() - start_time)))
    return


def turnToList(soup):
    table = []
    for i in soup:
        table.append(i.getText().split())
    return table
    

def main():
    crawl()

if __name__=='__main__':
      sys.exit(main())
