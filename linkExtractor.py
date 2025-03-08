#!/usr/bin/python3
import requests
from bs4 import BeautifulSoup
import hashlib
import argparse
from urllib.parse import urlsplit

def clean_text(x):
    BAD_CHARS = ['\n', '\t', ';']
    for bad_char in BAD_CHARS:
        x = x.replace(bad_char, "")
    return(x)

parser = argparse.ArgumentParser()
parser.add_argument('url')
args = parser.parse_args()
r = requests.get(args.url)
links_count = 0

filename = hashlib.md5(args.url.encode())
filename = 'hyperlinks_' + filename.hexdigest() + '.csv'

soup = BeautifulSoup(r.content, 'html.parser')
links = soup.find_all('a')

file = open(filename, 'a')
file.write('url;link;source_domain_name;target_domain_name;text\n')
for link in links:
    try:
        if link['href'][:4] == 'http':
            link_text = clean_text(link.text)
            domain_name_url = urlsplit(args.url).netloc.replace('www.', '')
            domain_name_href = urlsplit(link['href']).netloc.replace('www.', '')
            file.write(args.url + ';' + link['href'] + ';' + domain_name_url + ';' + domain_name_href + ';' + link_text + '\n')
            links_count = links_count + 1
    except:
        print('skip error')
    
file.close()
if links_count == 0:
    print('No hyperlink found !')
else:
    print(str(links_count) + ' hyperlinks found')
    print('File "' + filename + '" created successfully ...')



