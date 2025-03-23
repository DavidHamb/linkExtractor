#!/usr/bin/python3
import requests
from bs4 import BeautifulSoup
import time
import argparse
import re

parser = argparse.ArgumentParser()
parser.add_argument('url')
parser.add_argument('limit')
args = parser.parse_args()

url = args.url
limit = int(args.limit)

def convertHttp(url):
    if url[:5] == 'http:':
        url = url.replace('http:', 'https:')
    return(url)

def relativeToAbsoluteUrl(link, url):
    if link[:4] != 'http':
        link = url + link
    return(link)

def getLinksRecursively(url, limit):
    liste_url = [url]
    count = 0

    for u in liste_url:
        if count < limit:
            print('\n === Results for ' + u + ' === \n')
            time.sleep(2)
            r = requests.get(u)
            soup = BeautifulSoup(r.content, 'html.parser')
            links = soup.find_all('a')
            for link in links:
                if count < limit:
                    new_url = link['href']
                    new_url = convertHttp(new_url) # convert http to https
                    new_url = relativeToAbsoluteUrl(new_url, u) # convert relative to absolute
                    if new_url not in liste_url:
                        liste_url.append(new_url)
                        print(new_url)
                    count = count + 1

    print('\n Hyperlinks found: ' + str(count))

# main
if re.search(r'/$', url) == None:
    url = url + '/'
    
getLinksRecursively(url, limit)