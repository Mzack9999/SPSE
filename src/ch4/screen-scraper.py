#!/usr/bin/env python

# Author: SPSE-3232
# Purpose:
# - Create scrapers with beautifulsup to extract informations
# - medium.com posts

import requests
from bs4 import BeautifulSoup

r = requests.get('https://medium.com/xxx')

bs = BeautifulSoup(r.content, "html.parser")

print('Title: ', bs.title.encode('utf-8'))
for div in bs.findAll('p', {'class': 'graf'}):
    print(div.get_text().encode('utf-8'))