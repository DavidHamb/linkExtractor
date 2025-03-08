#!/usr/bin/python3
from selenium import webdriver
from selenium.webdriver.common.by import By
import argparse
import hashlib
from urllib.parse import urlsplit

# a function cleaning bad characters
def clean_text(x):
    BAD_CHARS = ['\n', '\t', ';']
    for bad_char in BAD_CHARS:
        x = x.replace(bad_char, "")
    return(x)

# set url as command line argument
parser = argparse.ArgumentParser()
parser.add_argument('url')
args = parser.parse_args()

# send the request to the url
browser = webdriver.Firefox()
browser.get(args.url)

# set link count to 0
links_count = 0

# create a file name
filename = hashlib.md5(args.url.encode())
filename = 'hyperlinks_' + filename.hexdigest() + '.csv'

# find all href attributes in all a tags
links = browser.find_elements(By.TAG_NAME, 'a')

# create a csv file
file = open(filename, 'a')
file.write('url;link;source_domain_name;target_domain_name;text\n')

for link in links:
    href = link.get_attribute('href')
    if href[:4] == 'http':
        try:
            link_text = clean_text(link.text)
            domain_name_url = urlsplit(args.url).netloc.replace('www.', '')
            domain_name_href = urlsplit(href).netloc.replace('www.', '')
            file.write(args.url + ';' + href + ';' + domain_name_url + ';' + domain_name_href + ';' + link_text + '\n')
            links_count = links_count + 1            
        except:
            print('skip error')

file.close()
if links_count == 0:
    print('No hyperlink found !')
else:
    print(str(links_count) + ' hyperlinks found')
    print('File "' + filename + '" created successfully ...')



# check same results as linkExtractor