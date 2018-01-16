#!/usr/bin/env python

# Author: SPSE-3232
# Purpose:
# - Read the documentation of BeautifulSoup 4
# - find other ways to iterate through tags and get to the juicy information

import requests
from bs4 import BeautifulSoup


r = requests.get('https://edition.cnn.com/')

bs = BeautifulSoup(r.content, "html.parser")

print('Title: ', bs.title.encode('utf-8'))
for head in bs.head:
    print('Head: ', head.encode('utf-8'))
for tag in bs.find_all('a'):
    print(tag.encode('utf-8'))