#! /usr/bin/env python3


from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import random
import requests
######################## Crawler Settings ####################### 


def setConfig():

    CONFIGS = []
    
    with open('../vault/.config','r') as f:
        data = f.readlines()
        for line in data:
            CONFIGS.append(line.strip().split())

    return CONFIGS

UA = UserAgent()               # generate a random user agent
TESTURL = setConfig()[2][1]        # first line second element
API_KEY = setConfig()[1][1]    # sets API key (scraperAPI)

######################## Crawler Settings #######################


def checkIP():
    #leq.set_proxy(FAKE_IP,'http')
    #req.add_header('User_Agent', UA.random)

    try:    

        payload = {'key': API_KEY, 'url': TESTURL}

        r = requests.get('http://api.scraperapi.com',params=payload)

        print(r.text)

    except: # If error, delete this proxy and find another one
        print('error when attempting request')
    
    return

def main():
    return checkIP()

if __name__ == '__main__':
    main()
